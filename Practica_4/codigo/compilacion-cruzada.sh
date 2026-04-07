#!/bin/bash

if [ $# -lt 1 ]; then
  echo "Numero de parametros incorrecto"
  echo "USO:"
  echo "  $0 FICHERO_FUENTE"
  exit 1
fi

DESTINO="$(basename $1 .c).s"
riscv64-linux-gnu-gcc -S -fverbose-asm -O0 -g0 -march=rv32im -mabi=ilp32 -fno-stack-protector $1 -o $DESTINO
if [ $? -eq 0 ]; then
  DIR="$(cd "$(dirname "$0")" && pwd)"
  python3 $DIR/limpia-asm.py -e $DESTINO
fi 



