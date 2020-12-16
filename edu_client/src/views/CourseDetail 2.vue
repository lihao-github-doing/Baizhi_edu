<template>
  <div class="detail">
    <Header/>
    <div class="main">
      <div class="course-info">
        <div class="wrap-left">
          <!--          <videoPlayer></videoPlayer>-->
          <videoPlayer class="video-player vjs-custom-skin"
                       ref="videoPlayer"
                       :playsinline="true"
                       :options="playerOptions"
                       @play="onPlayerPlay($event)"
                       @pause="onPlayerPause($event)">
          </videoPlayer>
        </div>
        <div class="wrap-right">
          <h3 class="course-name">{{ course.name }}</h3>
          <p class="data">{{ course.students }}人在学&nbsp;&nbsp;&nbsp;&nbsp;课程总时长：45课时/89小时&nbsp;&nbsp;&nbsp;&nbsp;
            难度：{{ course.level_name }}</p>
          <div class="sale-time">
            <p class="sale-type">{{ course.discount_name }}</p>
            <p class="expire">距离结束：仅剩 {{ parseInt(course.active_time / (24 * 3600)) }}天
              {{ parseInt(course.active_time / 3600 % 24) }}小时
              {{ parseInt(course.active_time / 60 % 60) }}分 <span
                  class="second">{{ parseInt(course.active_time % 60) }}</span> 秒
            </p>
          </div>
          <p class="course-price">
            <span>活动价</span>
            <span class="discount">¥{{ course.discount_price }}</span>
            <span class="original">¥{{ course.price }}</span>
          </p>
          <div class="buy">
            <div class="buy-btn">
              <button class="buy-now">立即购买</button>
              <button class="free">免费试学</button>
            </div>
            <div class="add-cart"><img src="/static/image/cart-yellow.svg" alt="">
              <span @click="add_cart">加入购物车</span>
            </div>
          </div>
        </div>
      </div>
      <div class="course-tab">
        <ul class="tab-list">
          <li :class="tabIndex==1?'active':''" @click="tabIndex=1">详情介绍</li>
          <li :class="tabIndex==2?'active':''" @click="tabIndex=2">课程章节 <span :class="tabIndex!=2?'free':''">(试学)</span>
          </li>
          <li :class="tabIndex==3?'active':''" @click="tabIndex=3">学生评论 (88)</li>
          <li :class="tabIndex==4?'active':''" @click="tabIndex=4">常见问题</li>
        </ul>
      </div>
      <div class="course-content">
        <div class="course-tab-list">
          <div class="tab-item" v-if="tabIndex==1">
            <div v-html="course.brief_html"></div>
          </div>
          <div class="tab-item" v-if="tabIndex==2">
            <div class="tab-item-title">
              <p class="chapter">课程章节</p>
              <p class="chapter-length">共8章 75个课时</p>
            </div>
            <div class="chapter-item">
              <p class="chapter-title"><img src="/static/image/1.svg" alt="">第1章·Vue简介</p>
              <ul class="lesson-list">
                <li class="lesson-item">
                  <p class="name"><span class="index">1-1</span> Vue基本介绍<span class="free">免费</span>
                  </p>
                  <p class="time">07:30 <img src="/static/image/chapter-player.svg"></p>
                  <button class="try">立即试学</button>
                </li>
                <li class="lesson-item">
                  <p class="name"><span class="index">1-2</span> Vue的双向绑定<span class="free">免费</span>
                  </p>
                  <p class="time">07:30 <img src="/static/image/chapter-player.svg"></p>
                  <button class="try">立即试学</button>
                </li>
              </ul>
            </div>
            <div class="chapter-item">
              <p class="chapter-title"><img src="/static/image/12.png" alt="">第2章·Vue发展过程</p>
              <ul class="lesson-list">
                <li class="lesson-item">
                  <p class="name"><span class="index">2-1</span> Vue脚手架</p>
                  <p class="time">07:30 <img src="/static/image/chapter-player.svg"></p>
                  <button class="try">立即购买</button>
                </li>
                <li class="lesson-item">
                  <p class="name"><span class="index">2-2</span> Vue的路由</p>
                  <p class="time">07:30 <img src="/static/image/chapter-player.svg"></p>
                  <button class="try">立即购买</button>
                </li>
              </ul>
            </div>
          </div>
          <div class="tab-item" v-if="tabIndex==3">
            用户评论
          </div>
          <div class="tab-item" v-if="tabIndex==4">
            常见问题
          </div>
        </div>
        <div class="course-side">
          <div class="teacher-info">
            <h4 class="side-title"><span>授课老师</span></h4>
            <div class="teacher-content">
              <div class="cont1">
                <img :src="course.teacher.image">
                <div class="name">
                  <p class="teacher-name">{{ course.teacher.name }}</p>
                  <p class="teacher-title">我永远18！</p>
                </div>
              </div>
              <p class="narrative">技术专家，百知教育金牌讲师，独有的闷骚气质撩到爆炸</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <Footer/>
  </div>
</template>

<script>

import {videoPlayer} from 'vue-video-player'
import Header from "@/components/Header";
import Footer from "@/components/Footer";

export default {
  name: "CourseDetail",
  data() {
    return {
      course_id: 0,
      tabIndex: 2,
      course: {
        teacher: {}
      },
      // 播放视频的配置
      playerOptions: {
        playbackRates: [0.7, 1.0, 1.5, 2.0], // 播放速度
        autoplay: false, //如果true,则自动播放
        muted: false, // 默认情况下将会消除任何音频。
        loop: false, // 循环播放
        preload: 'auto',  // 建议浏览器在<video>加载元素后是否应该开始下载视频数据。auto浏览器选择最佳行为,立即开始加载视频（如果浏览器支持）
        language: 'zh-CN',
        aspectRatio: '16:9', // 将播放器置于流畅模式，并在计算播放器的动态大小时使用该值。值应该代表一个比例 - 用冒号分隔的两个数字（例如"16:9"或"4:3"）
        fluid: true, // 当true时，Video.js player将拥有流体大小。换句话说，它将按比例缩放以适应其容器。
        sources: [{ // 播放资源和资源格式
          type: "video/mp4",
          src: "https://cdn.theguardian.tv/webM/2015/07/20/150716YesMen_synd_768k_vp8.webm"
          //你的视频地址（必填）
        }],
        poster: "../static/image/java_lesson.png", //视频封面图
        width: document.documentElement.clientWidth, // 默认视频全屏时的最大宽度
        notSupportedMessage: '此视频暂无法播放，请稍后再试', //允许覆盖Video.js无法播放媒体源时显示的默认信息。
      },
    }
  },
  methods: {

    // 检查用户是否登录
    check_user_login() {
      let token = localStorage.token || sessionStorage.token;
      if (!token) {
        let self = this;
        this.$confirm("对不起，请登录后再添加购物车", {
          callback() {
            self.$router.push("/login")
          },
        });
        return false
      }
      return token;
    },

    // 添加购物车
    add_cart() {
      let token = this.check_user_login();
      // 发起请求添加购物车
      this.$axios.post(this.$settings.HOST + "cart/option/", {
        course_id: this.course_id,
      }, {
        headers: {
          // 必须请求头中携带token "jwt token值"
          "Authorization": "jwt " + token,
        }
      }).then(res => {
        this.$message.success(res.data.message);
        // 向状态机提交动作来修改商品的总数
        this.$store.commit("add_cart", res.data.cart_length)
      }).catch(error => {
        console.log(error);
      })
    },

    onPlayerPlay() {
      alert("我是广告")
    },
    onPlayerPause() {
      alert("我是广告1")
    },

    // 获取课程id
    get_course_id() {
      let course_id = this.$route.params.id;
      if (course_id > 0) {
        this.course_id = parseInt(course_id)
      } else {
        let self = this;
        this.$alert("对不起，您访问的页面不存在", "百知教育", {
          callback() {
            self.$router.go(-1);
          }
        });
        return false;
      }
      return course_id;
    },

    // 获取当前课程的详细信息
    get_course_detail() {
      this.$axios({
        url: this.$settings.HOST + "course/detail/" + this.course_id + "/",
        method: 'get',
      }).then(res => {
        console.log(res.data);
        this.course = res.data;

        // 设置课程活动的倒计时
        if (this.course.active_time > 0) {
          let timer = setInterval(() => {
            if (this.course.active_time > 1) {
              this.course.active_time -= 1
            } else {
              clearInterval(timer)
            }
          }, 1000)
        }

      }).catch(error => {
        console.log(error);
      })
    },

    // 获取当前课程的章节信息
    get_course_chapter() {
    },
  },
  created() {
    this.get_course_id()
    this.get_course_detail()
  },
  components: {
    videoPlayer,
    Footer,
    Header
  }
}
</script>

<style scoped>
.main {
  background: #fff;
  padding-top: 30px;
}

.course-info {
  width: 1200px;
  margin: 0 auto;
  overflow: hidden;
}

.wrap-left {
  float: left;
  width: 690px;
  height: 388px;
  background-color: #000;
}

.wrap-right {
  float: left;
  position: relative;
  height: 388px;
}

.course-name {
  font-size: 20px;
  color: #333;
  padding: 10px 23px;
  letter-spacing: .45px;
}

.data {
  padding-left: 23px;
  padding-right: 23px;
  padding-bottom: 16px;
  font-size: 14px;
  color: #9b9b9b;
}

.sale-time {
  width: 464px;
  background: #84cc39;
  font-size: 14px;
  color: #4a4a4a;
  padding: 10px 23px;
  overflow: hidden;
}

.sale-type {
  font-size: 16px;
  color: #fff;
  letter-spacing: .36px;
  float: left;
}

.sale-time .expire {
  font-size: 14px;
  color: #fff;
  float: right;
}

.sale-time .expire .second {
  width: 24px;
  display: inline-block;
  background: #fafafa;
  color: #5e5e5e;
  padding: 6px 0;
  text-align: center;
}

.course-price {
  background: #fff;
  font-size: 14px;
  color: #4a4a4a;
  padding: 5px 23px;
}

.discount {
  font-size: 26px;
  color: #fa6240;
  margin-left: 10px;
  display: inline-block;
  margin-bottom: -5px;
}

.original {
  font-size: 14px;
  color: #9b9b9b;
  margin-left: 10px;
  text-decoration: line-through;
}

.buy {
  width: 464px;
  padding: 0px 23px;
  position: absolute;
  left: 0;
  bottom: 20px;
  overflow: hidden;
}

.buy .buy-btn {
  float: left;
}

.buy .buy-now {
  width: 125px;
  height: 40px;
  border: 0;
  background: #ffc210;
  border-radius: 4px;
  color: #fff;
  cursor: pointer;
  margin-right: 15px;
  outline: none;
}

.buy .free {
  width: 125px;
  height: 40px;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 15px;
  background: #fff;
  color: #ffc210;
  border: 1px solid #ffc210;
}

.add-cart {
  float: right;
  font-size: 14px;
  color: #ffc210;
  text-align: center;
  cursor: pointer;
  margin-top: 10px;
}

.add-cart img {
  width: 20px;
  height: 18px;
  margin-right: 7px;
  vertical-align: middle;
}

.course-tab {
  width: 100%;
  background: #fff;
  margin-bottom: 30px;
  box-shadow: 0 2px 4px 0 #f0f0f0;

}

.course-tab .tab-list {
  width: 1200px;
  margin: auto;
  color: #4a4a4a;
  overflow: hidden;
}

.tab-list li {
  float: left;
  margin-right: 15px;
  padding: 26px 20px 16px;
  font-size: 17px;
  cursor: pointer;
}

.tab-list .active {
  color: #ffc210;
  border-bottom: 2px solid #ffc210;
}

.tab-list .free {
  color: #fb7c55;
}

.course-content {
  width: 1200px;
  margin: 0 auto;
  background: #FAFAFA;
  overflow: hidden;
  padding-bottom: 40px;
}

.course-tab-list {
  width: 880px;
  height: auto;
  padding: 20px;
  background: #fff;
  float: left;
  box-sizing: border-box;
  overflow: hidden;
  position: relative;
  box-shadow: 0 2px 4px 0 #f0f0f0;
}

.tab-item {
  width: 880px;
  background: #fff;
  padding-bottom: 20px;
  box-shadow: 0 2px 4px 0 #f0f0f0;
}

.tab-item-title {
  justify-content: space-between;
  padding: 25px 20px 11px;
  border-radius: 4px;
  margin-bottom: 20px;
  border-bottom: 1px solid #333;
  border-bottom-color: rgba(51, 51, 51, .05);
  overflow: hidden;
}

.chapter {
  font-size: 17px;
  color: #4a4a4a;
  float: left;
}

.chapter-length {
  float: right;
  font-size: 14px;
  color: #9b9b9b;
  letter-spacing: .19px;
}

.chapter-title {
  font-size: 16px;
  color: #4a4a4a;
  letter-spacing: .26px;
  padding: 12px;
  background: #eee;
  border-radius: 2px;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-align: center;
  align-items: center;
}

.chapter-title img {
  width: 18px;
  height: 18px;
  margin-right: 7px;
  vertical-align: middle;
}

.lesson-list {
  padding: 0 20px;
}

.lesson-list .lesson-item {
  padding: 15px 20px 15px 36px;
  cursor: pointer;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
}

.lesson-item .name {
  font-size: 14px;
  color: #666;
  float: left;
}

.lesson-item .index {
  margin-right: 5px;
}

.lesson-item .free {
  font-size: 12px;
  color: #fff;
  letter-spacing: .19px;
  background: #ffc210;
  border-radius: 100px;
  padding: 1px 9px;
  margin-left: 10px;
}

.lesson-item .time {
  font-size: 14px;
  color: #666;
  letter-spacing: .23px;
  opacity: 1;
  transition: all .15s ease-in-out;
  float: right;
}

.lesson-item .time img {
  width: 18px;
  height: 18px;
  margin-left: 15px;
  vertical-align: text-bottom;
}

.lesson-item .try {
  width: 86px;
  height: 28px;
  background: #ffc210;
  border-radius: 4px;
  font-size: 14px;
  color: #fff;
  position: absolute;
  right: 20px;
  top: 10px;
  opacity: 0;
  transition: all .2s ease-in-out;
  cursor: pointer;
  outline: none;
  border: none;
}

.lesson-item:hover {
  background: #fcf7ef;
  box-shadow: 0 0 0 0 #f3f3f3;
}

.lesson-item:hover .name {
  color: #333;
}

.lesson-item:hover .try {
  opacity: 1;
}

.course-side {
  width: 300px;
  height: auto;
  margin-left: 20px;
  float: right;
}

.teacher-info {
  background: #fff;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px 0 #f0f0f0;
}

.side-title {
  font-weight: normal;
  font-size: 17px;
  color: #4a4a4a;
  padding: 18px 14px;
  border-bottom: 1px solid #333;
  border-bottom-color: rgba(51, 51, 51, .05);
}

.side-title span {
  display: inline-block;
  border-left: 2px solid #ffc210;
  padding-left: 12px;
}

.teacher-content {
  padding: 30px 20px;
  box-sizing: border-box;
}

.teacher-content .cont1 {
  margin-bottom: 12px;
  overflow: hidden;
}

.teacher-content .cont1 img {
  width: 54px;
  height: 54px;
  margin-right: 12px;
  float: left;
}

.teacher-content .cont1 .name {
  float: right;
}

.teacher-content .cont1 .teacher-name {
  width: 188px;
  font-size: 16px;
  color: #4a4a4a;
  padding-bottom: 4px;
}

.teacher-content .cont1 .teacher-title {
  width: 188px;
  font-size: 13px;
  color: #9b9b9b;
  white-space: nowrap;
}

.teacher-content .narrative {
  font-size: 14px;
  color: #666;
  line-height: 24px;
}
</style>
