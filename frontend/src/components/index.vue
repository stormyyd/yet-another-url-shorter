<template>
  <div id="index">
    <el-container>
      <el-header>
        <h1 class="title">一个简单的短链接生成器</h1>
      </el-header>
      <el-main>
        <el-row>
          <el-col :span="12" :offset="5">
            <el-input v-model="url" placeholder="请输入需要缩短的网址"/>
          </el-col>
          <el-col :span="2">
            <el-button type="primary" @click="generate">生成短链接</el-button>
          </el-col>
        </el-row>
        <template v-if="showResult">
          <el-row>
            <el-col :span="12" :offset="5">
              <p>
                <img :src="imgDataURL"/>
              </p>
              <p>
                <a :href="shortedURL">{{ shortedURL }}</a>
              </p>
            </el-col>
          </el-row>
        </template>
        <a href="https://github.com/stormyyd/yet-another-url-shorter"><img style="position: absolute; top: 0; right: 0; border: 0;" src="https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png" alt="Fork me on GitHub"></a>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import axios from 'axios'
import QRCode from 'qrcode'

export default {
  data() {
    return {
      url: '',
      shortedURL: '',
      showResult: false,
      imgDataURL: '',
    }
  },
  methods: {
    generate: async function() {
      if(this.url.substr(0, 7) != 'http://' && this.url.substr(0, 8) != 'https://') {
        this.$alert('请确定您输入的链接以 http:// 或 https:// 开头', '地址不合法', {
          confirmButtonText: '确定'
        })
      }
      var result = await axios.post('/api/new', {
        url: this.url
      })
      if('error' in result) {
        this.$alert('未知错误', '错误', {
          confirmButtonText: '确定'
        })
      }
      this.shortedURL = `${ window.location.protocol }//${ window.location.host }/${ result.data.shorted_url }`
      this.imgDataURL = await QRCode.toDataURL(this.shortedURL)
      this.showResult = true
    }
  }
}
</script>

<style>
a:hover, a:visited, a:link, a:active {
  text-decoration: none;
  color: #409EFF;
}

h1.title {
  color: #303133;
}
</style>
