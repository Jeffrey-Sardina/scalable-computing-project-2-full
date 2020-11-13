param
(
    [string]$inputModel=""
)

echo 'starting trainimg'

if($inputModel -eq "")
{
    python train.py --width 128 --height 64 --length 6 --symbols model/symbols.txt --batch-size 32 --epochs 100 --output-model-name model/model --train-dataset model/gen/ --validate-dataset model/val/
}
else
{
    python train.py --width 128 --height 64 --length 6 --symbols model/symbols.txt --batch-size 32 --epochs 100 --output-model-name model/model --train-dataset model/gen/ --validate-dataset model/val/ --input-model $inputModel
}

if (!$?)
{
    exit 1
}
else
{
    exit 0
}
