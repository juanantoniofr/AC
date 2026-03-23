#
# Limpia el código ensamblador del RISC-V generado por gcc para que 
# pueda ser simulado en el RARS
# 
# Autor: Ignacio García Vargas
#
# USO: limpia-asm.py [-e] nombre_archivo.s
#
# La opción -e elimina el marco de pila de la función main.
#
import sys
import re
import os

finmain = """
    # --- Fin del programa (Syscall Exit) ---
    li a7, 10          # Código 10: Salir
    ecall
"""

def limpiar_ensamblador(archivo_entrada, archivo_salida):
    # Directivas de GCC que RARS no reconoce o que ensucian el código
    ignorar = [
        r'\.file', r'\.attribute', r'\.option', r'\.type', 
        r'\.size', r'\.ident', r'\.section', r'\.align',
        r'\.cfi_', r'\.addrsig', r'\.globl.*', #, r'\.globl\s+main' # La reañadimos nosotros a mano
        r'^#.*GNU.*', r'^#\s+GGC\s+heuristics:', r'^#\s+options\s+passed:'
    ]
    
    sustituir = {
        'lla':'la', 
        'call':'jal ra,', 
        '.zero':'.space', 
        '.bss': '.data'
    }
    
    try:
        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo_entrada}'")
        return

    lineas_limpias = []
    enmain = False
    nuevo_marco_pila = False
    inicio_marco_pila = 0
    len_marco_pila = 0
    
    for linea in lineas:
        contenido = linea.strip()
        linea = linea.rstrip()
        # Elimina comentarios al final de las líneas
        if contenido.find('#') > 0:
            linea = linea[:linea.find('#')]
            contenido = linea.strip()
                        
        # Saltamos líneas vacías o directivas que no queremos
        if not contenido or any(re.match(d, contenido) for d in ignorar):
            continue
            
        if contenido == '.text':
            lineas_limpias.append('\n\t# Segmento de código')
            lineas_limpias.append(linea)
            continue
            
        if contenido == '.data':
            lineas_limpias.append('\n\t# Segmento de datos')
            lineas_limpias.append(linea)
            continue
        
        # Añade .globl main
        if contenido == "main:":
            lineas_limpias.append(".globl main")
            lineas_limpias.insert(0, "\tj main\n")
            lineas_limpias.insert(0, "\t# Llama a la función main (esta línea no es necesaria si RARS se configura para ejecutar primero el main")
            enmain = True
            len_marco_pila = 0
        
        # Sustituir la instrucción "jr ra" del main por la secuencia finalizar el programa
        if enmain and re.match(r'jr\s+ra', contenido):
            linea = finmain
            # ~ enmain = False
            
        if contenido.startswith('.LFB'):
            # inicio de función (detectamos marco de pila)
            nuevo_marco_pila = True
            lineas_limpias.append("\t# Crea el nuevo marco de pila de la función")
            inicio_marco_pila = len(lineas_limpias)
            continue
            
        if nuevo_marco_pila and re.match(r'addi\s+s0,sp', contenido):
            nuevo_marco_pila = False
            lineas_limpias.append(linea)
            len_marco_pila = len(lineas_limpias) - inicio_marco_pila
            if enmain and elimina_marco_pila:
                # Eliminamos el marco de pila
                del lineas_limpias[-len_marco_pila:]
            lineas_limpias.append("\t# Fin de la creación del nuevo marco de pila")
            continue
                            
        if contenido.startswith('.LFE'):
            if enmain and elimina_marco_pila:
                # Elimina las instrucciones del marco de pila del main
                #del lineas_limpias[-2:-1]
                enmain = False
                del lineas_limpias[-len_marco_pila:-1]
                lineas_limpias.insert(-1, "\t# Restaura el marco de pila anterior")
                lineas_limpias.insert(-1, "\t# Fin de la restauración del marco de pila")
            else:
                lineas_limpias.insert(-len_marco_pila, "\t# Restaura el marco de pila anterior")
                lineas_limpias.insert(-1, "\t# Fin de la restauración del marco de pila")
            continue

        # Sustituye algunas instrucciones:
        for k,v in sustituir.items():
            if contenido.startswith(k):
                linea = linea.replace(k,v)
                                    
        # Limpieza de etiquetas de metadatos (como las que empiezan por L)
        # Solo mantenemos etiquetas útiles o instrucciones
        lineas_limpias.append(linea)

    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write("\n".join(lineas_limpias))

if __name__ == "__main__":
    numarg = len(sys.argv)
    if numarg < 2 or numarg > 3 or (numarg == 2 and sys.argv[1] == '-e') or (numarg == 3 and sys.argv[1] != '-e'):
        print(f"USO: \n\tpython3 {sys.argv[0]} [-e] nombre_archivo.s")
        sys.exit(1)
    if sys.argv[1] == '-e':
        elimina_marco_pila = True
        nombre_entrada = sys.argv[2]
    else:
        elimina_marco_pila = False
        nombre_entrada = sys.argv[1]
    if not os.path.exists(nombre_entrada):
        print(f'Error: el archivo no existe: {nombre_entrada}')
        sys.exit(1)
    nombre_salida = "rars_" + nombre_entrada
    limpiar_ensamblador(nombre_entrada, nombre_salida)
    os.replace(nombre_entrada, f'{nombre_entrada}aux')
    print(f"Archivo para RARS generado: {nombre_salida}")
