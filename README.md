# volmoe-pack

pack comic volumes for vol.moe

## Usage

```bash
python3 pack.py -h
```

准备好文件夹：

```
123
├── 第01回
│   ├── 001.jpg
│   ├── 002.jpg
│   ├── 003.jpg
├── 第02回
│   ├── 001.jpg
│   ├── 002.jpg
├── 第03回
│   ├── 001.jpg
│   ├── 002.jpg
│   ├── 003.jpg
├── 第04回
│   ├── 001.jpg
│   ├── 002.jpg
├── 第05回
│   ├── 001.jpg
│   ├── 002.jpg
│   ├── 003.jpg
├── 第06回
│   ├── 001.jpg
├── 第07回
│   ├── 001.jpg
│   ├── 002.jpg
├── 第08回
│   ├── 001.jpg
│   ├── 002.jpg
│   ├── 003.jpg
├── 第09回
│   ├── 001.jpg
│   ├── 002.jpg
│   ├── 003.jpg
│   ├── 004.jpg
├── 第10回
│   ├── 001.jpg
│   ├── 002.jpg
│   ├── 003.jpg
├── 第11回
│   ├── 001.jpg
│   ├── 002.jpg
│   ├── 003.jpg
├── 第12回
│   ├── 001.jpg
│   ├── 002.jpg
│   ├── 003.jpg

├── 第13回
│   ├── 001.jpg
│   ├── 002.jpg
│   ├── 003.jpg
├── 第14回
│   ├── 001.jpg
│   ├── 002.jpg

├── 第15回
│   ├── 001.jpg

```

运行

```bash
python3 pack.py -o output 123
ls output/
```
