# pysimple


<i>Utils for other projects ...</i>


## Install


```
$ git clone https://github.com/tarashypka/pysimple.git && cd pysimple
$ chmod +x install.sh && ./install.sh --conda=/path/to/anaconda --env=ENV_NAME
```

This will

- create new conda environment at `/path/to/anaconda/envs/ENV_NAME`;
- install all requirements into environment;
- run all tests from `pysimple/tests`;
- if all tests passed, then install `pysimple` module into environment
