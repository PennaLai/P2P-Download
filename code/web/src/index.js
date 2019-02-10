import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import registerServiceWorker from './registerServiceWorker';
// new
import axios from 'axios';
import {message, Card, Col, Row, Upload, Button, Icon, Input, Modal, Alert, Layout, Menu, Breadcrumb, Table, Divider} from 'antd';



const { Header, Content, Footer } = Layout;
const Search = Input.Search; // 搜索框


class SearchPage extends Component{
	constructor() {
        super();
        this.recvData = this.recvData.bind(this);
    }

	state={
		hasData : true,
		fileName: '',
		infos:[],
		download_urls: [],
		columns :[ {
				  title: 'UUID',
				  dataIndex: 'uuid',
				  key: 'uuid',
				  render: text => <div>{text}</div>,
				}, {
				  title: 'Torrent',
				  dataIndex: 'torrent_url',
				  key: 'torrent_url',
				  render: text => <a href={text}>{text}</a>,
				},{
				  title: 'Download',
				  dataIndex: 'file_url',
				  key: 'file_url',
				  render: file_url => 
				  <Button type="primary" href={file_url} onClick={this.DownloadSuccess}shape="circle" icon="download" size='large' />
				}],
	}

	// 将每一段集合成一个blob对象，然后返回
	DownloadFile = e =>{
		// message.info('downloading....');
		let buffer = new Array(this.state.chunks_size)
		for(var i=0; i<this.state.download_urls.length;i++){
			let url = this.state.download_urls[i];
			let part = this.one_part(url, 0, 30)
			buffer[i] = part
		}
        let blob = new Blob(buffer)	// 合成后的对象4
       if ('download' in document.createElement('a')) { // 非IE下载
          const elink = document.createElement('a')
          elink.download = 'filename'
          elink.style.display = 'none'
          elink.href = URL.createObjectURL(blob)
          document.body.appendChild(elink)
          elink.click()
          URL.revokeObjectURL(elink.href) // 释放URL 对象
          document.body.removeChild(elink)
        } else { // IE10+下载
          navigator.msSaveBlob(blob, 'fileName')
        }
	}	


	// 单独获取一个链接的文件（其中一段）
	one_part(url, offset, length){
		let dlaxio = axios.create({
	    url: url,
	    method: 'post',
	    responseType: 'blob',
	    headers: {
	    	'Range': 'bytes={offset}-{offset+length-1}'
	    }
	  })
		return dlaxio.request(url)
	}					


	recvData(text){
		let rece_data = null;
		var that =this;
		let  url="http://10.21.72.153:5000/api/query?torrent="+text 	// 需要修改成自己主机的IP地址
			axios.get(url)
			  .then(function (response) {
			  	rece_data = response.data;
			  	// console.log(rece_data);
			  	  that.setState({
				  hasData : true,
				  fileName:response.data.name,
				  infos:response.data.info,
				  download_urls:response.data.download_urls
				 });
			  })
		  .catch(function (error) {	
		    console.log(error);
		  });
		
	}

	DownloadSuccess= e =>{
		message.info('downloading....' );

	}
	render() {
		return (
			  <div>
			<Search
			      placeholder="Input UUID"
			      onSearch={this.recvData}
			      style={{ width: 600, marginBottom:20}}
			    />
		 	      {(() => {
			        if (this.state.hasData) {
			          return <div>
			          <Table columns={this.state.columns} dataSource={this.state.infos} />
			          </div>
			        } else {
			          return <div></div>
			        }
		      })()}
			 </div>
		);
	}	
}	


 // 上传设置，需要修改成自己的IP地址
  const uploads = {
	  action: 'http://10.21.72.153:5001/api/upload',
	  onChange({ file, fileList }) {
	    if (file.status !== 'uploading') {
	      console.log(file, fileList);
	    }
	    headers:{
	    	Expect:"100-continue"
	    }
	  },
	  // 默认已上传的文件
	  defaultFileList: [],
	  	
	};


class MainLayout extends Component{
	 state = {
    current: '1',
  }

  handleClickMenu = (e) => {
    console.log('click ', e);
    this.setState({
      current: e.key,
    });
  }
 

	render() {
		return (

<Layout className="layout" style={{height:"100vh"}} >
    <Header>
     <div className="logo" />
      <Menu
        theme="dark"
        mode="horizontal"
        onClick={this.handleClickMenu}
        selectedKeys={[this.state.current]}
        defaultSelectedKeys={['1']}
        style={{ lineHeight: '64px' }}
      >
        <Menu.Item key="1">Upload</Menu.Item>
        <Menu.Item key="2">Search</Menu.Item>
         <Menu.Item key="3">Server</Menu.Item>
      </Menu>
    </Header>
	<Content style={{ padding: '0 50px' }}>
      <div>
      {(() => {
        if (this.state.current == 1) {
          return <div style={{ background: '#fff', padding: 24, minHeight: 280, height:"100vh"  }}> 
				      <Upload {...uploads}>
							    <Button >
							      <Icon type="upload" /> Click to Upload
							    </Button>
					  </Upload>
		 		</div>	
        } else if (this.state.current == 2) {
          return <div style={{ background: '#fff', padding: 24, minHeight: 280, height:"100vh" }}> 
	          	<SearchPage />
           </div>	
        }else{
        	 return <div style={{ background: '#fff', padding: 24, minHeight: 280, height:"100vh" }}> 
	      
           </div>	
        }
      })()}
    </div>
      
    </Content>
    <Footer style={{ textAlign: 'center' }}>
      Computer Network P2P Download ©2018 Created by 11610702
    </Footer>
</Layout>

		);
	}
}


ReactDOM.render(
	<MainLayout />,	
  document.getElementById('root')
)
		
registerServiceWorker();
