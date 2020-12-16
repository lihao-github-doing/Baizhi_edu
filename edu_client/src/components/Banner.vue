<template>
  <el-carousel height="720px" :interval="3000" arrow="always">
    <el-carousel-item v-for="(banner, index) in banner_list" :key="index">
      <a :href="banner.link"><img :src="banner.img"></a>
    </el-carousel-item>
  </el-carousel>
</template>

<script>
export default {
  name: "Banner",
  data() {
    return {
      banner_list: [],
    }
  },
  methods: {
    // 获取轮播图
    get_all_banner() {
      this.$axios({
        url: this.$settings.HOST + "home/banners/",
        method: 'get',
      }).then(response => {
        this.banner_list = response.data;
      }).catch(error => {
        console.log(26, error);
        this.$message({
          message: '地址错误',
          type: 'error',
          duration: 1000,
          showClose: true,
        });
      })
    },
  },
  created() {
    this.get_all_banner()
  },
}
</script>

<style scoped>
.el-carousel__item h3 {
  color: #475669;
  font-size: 18px;
  opacity: 0.75;
  line-height: 100px;
  margin: 0;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n+1) {
  background-color: #d3dce6;
}
</style>