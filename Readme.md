#  P2P程序使用说明

### 运行环境需求

请在满足以下环境下运行程序

#### 后端
- python 3.6
- flask

#### 前端
- react

#### 特别说明

因为前后端建立在不同的端口号上，并且本程序目前处于开发测试阶段，所以在普通浏览器运行可能会遇到跨域问题，请将chrome按照以下方式设置（大概30秒可设置完毕）

https://www.cnblogs.com/laden666666/p/5544572.html 

### 开始

###### tracker

选择一台主机作为tracker服务器，运行程序目录下的tracker.py， 并记录服务器IP地址

###### client

1. 运行程序目录下的client.py

2. 在client主机上，将client_main.py 里的第17行, 替换成对应tracker的主机IP地址

   ``` python
   app.config['TRACKER'] = 'http://x.x.x.x:5000'
   ```

3. 在client 上，将web目录下的src/index.js 里第89行更改成对应tracker的主机IP地址

   ``` javascript
   let  url="http://x.x.x.x:5000/api/query?torrent="+text
   ```

4. 在client上，将web目录下的src/index.js 里第136行改成自己client的IP地址！！！注意是client的
  ```javascript
  action: 'http://y.y.y.y:5001/api/upload'
  ```

5. 在web目录下运行命令行

   ``` shell
   npm start
   ```

   

6. 打开http://localhost:3000/

   - 上传
     - 点击上传图标，上传对应想要文件
     - 上传完毕后，在本地client/local_file的目录下可以看到刚刚放上的文件，以及生成的种子
     - 种子里面有对应的encryption信息
   - 查询
     - 只要获得了对应文件的encryption信息，即可在web下的搜索页面，输入encryption进行查询
     - 点击查询后能看到对应文件的三个信息（上传者，种子链接，下载链接）
     - 然后进行下载操作

