<template>
  <div class="footer">
    <ul >
      <li v-for="(nav,index) in nav_list" :key="index"><a :href="nav.link" style="color: #ffffff">{{nav.title}}</a></li>
<!--      <li>123123</li>-->
<!--      <li>关于我们</li>-->
<!--      <li>联系我们</li>-->
<!--      <li>百知教育</li>-->
<!--      <li>帮助中心</li>-->
<!--      <li>意见反馈</li>-->
<!--      <li>新手指南</li>-->
    </ul>
  </div>
</template>

<script>
export default {
  name: "Footer",
  data() {
    return {
      nav_list: [],
    }
  },
  methods: {
    // 获取所有轮播图的方法
    get_all_nav() {
      this.$axios({
        url: this.$settings.HOST + "home/navFoot/",
        method: 'get',
      }).then(res => {
        this.nav_list = res.data
      }).catch(error => {
        console.log(error)
      })
    },
  },
  created() {
    this.get_all_nav()
  },
}
</script>

<style scoped>

.footer {
  width: 100%;
  height: 128px;
  background: #25292e;
  color: #fff;
}

.footer ul {
  margin: 0 auto 16px;
  padding-top: 38px;
  width: 810px;
}

.footer ul li {
  float: left;
  width: 112px;
  margin: 0 10px;
  text-align: center;
  font-size: 14px;
}

.footer ul::after {
  content: "";
  display: block;
  clear: both;
}

.footer p {
  text-align: center;
  font-size: 12px;
}
</style>
