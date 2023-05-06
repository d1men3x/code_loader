# code_loader by d1men3x

Simple tool/module that make your deploy to unsecure places a litlle bit secure.


## Installing

```shell
git clone https://github.com/d1men3x/code_loader
cd code_loader
pip3 install -r requirements.txt
```

Now you can use code_loader


## CLI Usage

In this situation you can store code in encrypted state and execute only when it needed.

Encrypting your sources:

```shell
./payload_maker.py ./example/source.py ./example/source.bin
```

Output:

```plain
[?] Enter key for encryption(empty for random): 
[*] Encryption key not provided, they will be generated randomly
[+] Payload was successfully created
[*] Encryption key: J1k1DpfLjOK50P419gfXP8lX1N[:E2n3
```

Also you can provide key directly:
```shell
./payload_maker.py ./example/source.py ./example/source.bin "J1k1DpfLjOK50P419gfXP8lX1N[:E2n3"
```


Executing your sources:

```shell
./loader.py ./example/source.bin
[?] Enter encryption key: 
```

Output:

```plain
[*] Payload decrypted. Executing..
<     13 - 7 = 6    >>>>>

```

As in payload_maker, here you can provide key directly:
```shell
./loader.py ./example/source.bin "J1k1DpfLjOK50P419gfXP8lX1N[:E2n3"
```

But in this situation your key can be view via top/htop utility

> ***Impotant note: If you execute/generate payload from shell and provide key directly, don't forget clear history file, otherwise this tool becomes useless***



## Using as a module

In the progress...


## How it works?

Making payload from your code looking like this:

`Source Code -> Comiled Python Byte-Code -> Dumped Python Byte-Code -> Encrypted data`

Executing payload:

`Encrypted data -> Dumped Python Byte-Code -> Compiled Python Byte-Code -> Executing Python Byte-Code`

As you can see, it is very simple [^_^]


## Copyrights and other

Do with it code whatever you want. No Licence.
