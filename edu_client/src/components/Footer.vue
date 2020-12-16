<template>
  <div class="footer">
    <ul>
      <!--            <li v-for="(nav,index) in navs_list" :key='index'><a :href="nav.link">{{ nav.title }}</a></li>-->
      <li v-for="(date,index) in navs_list" :key="index"><a :href="date.link" target="_self"
                                                            v-if="date.is_site">{{ date.title }}</a>
        <router-link :to="date.link" v-else>{{ date.title }}</router-link></li>

        <!--      </li>-->
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
      navs_list: [],
    }
  },
  methods: {
    get_all_navs() {
      this.$axios({
        url: this.$settings.HOST + "home/navss/",
        method: 'get',
      }).then(response => {
        this.navs_list = response.data;
      }).catch(error => {
        console.log(30, error);
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
    this.get_all_navs()
  },
}
</script>

<style scoped>
.class1 {
  color: red;
}

.footer {
  width: 100%;
  height: 128px;
  background: white;
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