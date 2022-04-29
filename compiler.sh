#!/bin/bash

DIR=$(pwd)
WORK_DIR=/home/koda/study/docker/latex/compiler/two

compile_latex () {
    TEX=$1
    NAME_TEX=${TEX##*/}
    NAME=${NAME_TEX%.*}

    cp ./$NAME_TEX $WORK_DIR/files/hoge.tex
    if [ -e ./figures ]; then
	# 前回のコンパイル時のデータが残っている場合消す
        if [ -e $WORK_DIR/files/figures ]; then
            rm -r $WORK_DIR/files/figures
	fi
        cp -r ./figures $WORK_DIR/files/figures
    fi

    if [ -e ./sources ]; then
	# 前回のコンパイル時のデータが残っている場合消す
        if [ -e $WORK_DIR/files/sources ]; then
            rm -r $WORK_DIR/files/sources
	fi
        cp -r ./sources $WORK_DIR/files/sources
    fi

    cd $WORK_DIR/files
    docker run -itd --name latex_ mf220061/my_repository:latexv1.1
    docker cp ./ latex_:/root/result
    docker exec latex_ platex hoge && dvipdfmx hoge
    docker cp latex_:/root/result/ ./
    docker rm -f latex_

    cd $DIR
    cp $WORK_DIR/result/hoge.pdf ./$NAME.pdf
}

if [ $# -lt 1 ]; then
    TARGET=$(find . -name \*.tex)
    compile_latex $TARGET
else
    for TARGET in $@
    do
        compile_latex $TARGET
    done
fi
