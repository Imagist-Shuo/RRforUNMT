#!/bin/bash
set -e

WORK_PATH=your path
DATA_PATH=your path
RUN_T2T=$WORK_PATH/rewriting model/code
MOSES_PATH=moses path

MODE=$1
LANG_SRC=$2
LANG_TRG=$3
DEVISES=$4

#echo $MODE $ROUND $LANG_SRC $LANG_TRG $SHARE_BPE $DEVISES

LANG_DIRECTION=$LANG_SRC-$LANG_TRG
if [ $LANG_TRG == "en" ]
then
LANG_PAIR=$LANG_TRG-$LANG_SRC
else
LANG_PAIR=$LANG_SRC-$LANG_TRG
fi

MODEL=$DATA_PATH/Model/model_${LANG_DIRECTION}


if [ $MODE == "train" ]
then

VOCAB_SRC=$DATA_PATH/Vocab/$LANG_PAIR.$LANG_TRG.vocab
VOCAB_MEM=$DATA_PATH/Vocab/$LANG_PAIR.$LANG_TRG.vocab
VOCAB_TRG=$DATA_PATH/Vocab/$LANG_PAIR.$LANG_TRG.vocab

EMB_MEM=$DATA_PATH/Vocab/$LANG_PAIR.$LANG_TRG.vec

TRAIN_SRC=$DATA_PATH/Train/$LANG_PAIR.src.noi.$LANG_TRG
TRAIN_MEM=$DATA_PATH/Train/$LANG_PAIR.mem.$LANG_TRG
TRAIN_TRG=$DATA_PATH/Train/$LANG_PAIR.trg.$LANG_TRG
TRAIN_PARAMS="renew_lr=False,use_pretrained_embedding=True,shared_source_target_embedding=True,device_list=$DEVISES,train_steps=200000,batch_size=1024,save_checkpoint_steps=8000"

echo "==============================================================="
echo "Source file:" $TRAIN_SRC
echo "Memory file:" $TRAIN_MEM
echo "Target file:" $TRAIN_TRG
echo "Vocab files:" $VOCAB_SRC $VOCAB_MEM $VOCAB_TRG
echo "Embedding files:" $EMB_MEM
echo "Model folder:" $MODEL
echo "Training params:" $TRAIN_PARAMS
echo "==============================================================="

#python3 $RUN_T2T/scripts/shuffle_dataset.py --input $TRAIN_SRC $TRAIN_TRG

echo "Start Training........"
python3 $RUN_T2T/train.py --input $TRAIN_SRC $TRAIN_MEM $TRAIN_TRG \
    --output $MODEL \
    --vocab $VOCAB_SRC $VOCAB_MEM $VOCAB_TRG \
    --embeddings $EMB_MEM \
    --parameters=$TRAIN_PARAMS

elif [ $MODE == "test" ]
then

SRC_FILE=$5
MEM_FILE=$6
TRANS_FILE=$SRC_FILE.trans

VOCAB_SRC=$DATA_PATH/Vocab/$LANG_PAIR.$LANG_TRG.vocab
VOCAB_MEM=$DATA_PATH/Vocab/$LANG_PAIR.$LANG_SRC.vocab
VOCAB_TRG=$DATA_PATH/Vocab/$LANG_PAIR.$LANG_TRG.vocab

EMB_MEM=$DATA_PATH/Vocab/$LANG_PAIR.$LANG_SRC.vec

TEST_PARAMS="use_pretrained_embedding=False,device_list=$DEVISES,decode_batch_size=32,beam_size=8,decode_alpha=0.6"

echo "==============================================================="
echo "Source file:" $SRC_FILE $MEM_FILE
echo "Target file:" $TRANS_FILE
echo "Vocab files:" $VOCAB_SRC $VOCAB_MEM $VOCAB_TRG
echo "Model folder:" $MODEL
echo "Test params:" $TEST_PARAMS
echo "==============================================================="

echo "Start Testing........."
python3 $RUN_T2T/translate.py --input $SRC_FILE $MEM_FILE \
    --output $TRANS_FILE \
    --vocab $VOCAB_SRC $VOCAB_MEM $VOCAB_TRG \
    --models $MODEL \
    --parameters=$TEST_PARAMS

fi
