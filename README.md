### Using ggmlv3..bin model files

Convert the ggmlv3 model files with the `.scripts/convert.py`
script with the following command. ADJUST THE PARAMETERS OF THE COMMAND!

```
python3 ./convert.py --eps 1e-5 --input ./WizardLM-7B-uncensored.ggmlv3.q2_K.bin --output ./WizardLM-7B-uncensored.gguf.q2_K.bin
```