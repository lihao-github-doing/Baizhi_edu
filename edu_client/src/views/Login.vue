<template>
  <div class="login box">
    <img src="../static/image/1111.jpg" alt="">
    <div class="login">
      <div class="login-title">
        <img src="../static/image/logo.png" alt="">
        <p>百知教育给你最优质的学习体验!</p>
      </div>
      <div class="login_box">
        <div class="title">
          <span @click="add1">密码登录</span>
          <span @click="add2">短信登录</span>
        </div>
        <div class="inp" v-if="user1">
          <input type="text" placeholder="用户名 / 手机号码 / 邮箱" class="user" v-model="username">
          <input type="password" name="" class="pwd" placeholder="密码" v-model="password">
          <div id="captcha"></div>
          <div class="rember">
            <p>
              <input type="checkbox" class="no" v-model="remember_me"/>
              <span>记住密码</span>
            </p>
            <p>忘记密码</p>
          </div>
          <button class="login_btn btn btn-primary" @click="get_captcha">登录</button>
          <p class="go_login">没有账号
            <router-link to="/register">立即注册</router-link>
          </p>
        </div>
        <div class="inp" v-show="user2">
          <input type="text" placeholder="手机号码" class="user" v-model="phone" @blur="check_phone">
          <div class="sms-box">
            <input v-model="code" type="text" maxlength="6" placeholder="输入验证码" class="user">
            <div class="sms-btn" @click="phone_captcha" id="time">获取验证码<span v-if="disp">-{{ time }}秒</span></div>
          </div>
          <button class="login_btn" @click="user_logins">登录</button>
          <span class="go_login">没有账号
                    <router-link to="/register">立即注册</router-link>
                </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      username: '',
      password: '',
      remember_me: false,
      user1: true,
      user2: false,
      phone: '',
      code: '',
      disp: false,
      time: 60,
      phone_flag: false,
    }
  },
  created() {
    let username = localStorage.getItem('username')
    let password = localStorage.getItem('password')
    if (username && password) {
      this.username = username
      this.password = password
      this.remember_me = true
    }
  },

  methods: {
    check_phone() {
      this.$axios({
        url: this.$settings.HOST + "user/phone_code/",
        method: 'post',
        data: {
          phone: this.phone,
        }
      }).then(response => {
        console.log(response)
        this.phone_flag = true
      }).catch(error => {
        console.log(error)
        this.$message({
          message: "手机号不正确",
          type: 'success',
          duration: 2000,
          showClose: true,
        })
      })
    },

    clock: function () {
      this.disp = true
      this.times = setInterval(() => {
        this.time--
        if (this.time === 0) {
          this.disp = false
          clearInterval(this.times)
        }
      }, 1000)
    },
    phone_captcha() {
      if (this.phone === '') {
        this.$message({
          message: "手机号不能为空",
          type: 'success',
          duration: 2000,
          showClose: true,
        })
      } else if (this.phone_flag) {
        this.$axios({
          url: this.$settings.HOST + 'user/message/',
          method: 'get',
          params: {
            phone: this.phone,
          }
        }).then(response => {
          console.log(response)
          this.clock()
        }).catch(error => {
          console.log(error)
          this.$message({
            message: "验证码错误",
            type: 'success',
            duration: 2000,
            showClose: true,
          })
        })
      }
    },


    user_logins() {
      if (this.phone === '' || this.code === '') {
        this.$message({
          message: "手机号或验证码不能为空",
          type: 'success',
          duration: 2000,
          showClose: true,
        })
      } else if (this.check_phone) {
        this.$axios({
          url: this.$settings.HOST + 'user/phone_login/',
          method: 'post',
          data: {
            phone: this.phone,
            code: this.code
          }
        }).then(response => {
          let self = this;
          this.$alert("登录成功", "百知教育", {
            callback() {
              self.$router.push("/")
            }
          })
          localStorage.setItem('token', response.data.data.token)
          sessionStorage.setItem('token', response.data.data.token)
          localStorage.setItem('username', this.phone)
          sessionStorage.setItem('username', this.phone)
        }).catch(error => {
          console.log(error)
          this.$message({
            message: "手机号或密码或验证码不正确",
            type: 'success',
            duration: 2000,
            showClose: true,
          })
        })
      }
    },


    // 点击登录按钮式 获取滑块验证码
    get_captcha: function () {
      if (this.username === '' || this.password === '') {
        this.$message({
          message: "账号或密码不能为空",
          type: 'success',
          duration: 2000,
          showClose: true,
        })
      }
      this.$axios({
        url: this.$settings.HOST + "user/captcha/",
        method: 'get',
        params: {
          username: this.username,
        }
      }).then(res => {
        let data = JSON.parse(res.data);
        // 使用initGeetest接口
        // 参数1：配置参数
        // 参数2：回调，回调的第一个参数验证码对象，之后可以使用它做appendTo之类的事件
        initGeetest({
          gt: data.gt,
          challenge: data.challenge,
          product: "popup", // 产品形式，包括：float，embed，popup。注意只对PC版验证码有效
          offline: !data.success, // 表示用户后台检测极验服务器是否宕机，一般不需要关注
          new_captcha: data.new_captcha
        }, this.handlerPopup);
      }).catch(error => {
        console.log(error);
        this.$message({
          message: "用户名或密码错误",
          type: 'success',
          duration: 2000,
          showClose: true,
        })
      })
    },

    // 请求验证码的回调函数 完成验证码的验证码
    handlerPopup(captchaObj) {
      // 在回调函数中 this的指向会被改变
      let self = this;
      captchaObj.onSuccess(function () {
        let validate = captchaObj.getValidate();
        console.log(validate.geetest_challenge)
        self.$axios({
          url: self.$settings.HOST + "user/captcha/",
          method: "post",
          data: {
            geetest_challenge: validate.geetest_challenge,
            geetest_validate: validate.geetest_validate,
            geetest_seccode: validate.geetest_seccode
          },
        }).then(res => {
          console.log(res.data);
          // 如果滑块验证码的验证结果为True，则完成登录
          if (res.data.status) {
            self.user_login();
          }
        }).catch(error => {
          console.log(error);
        })
      })
      // 将验证码加到id为captcha的元素里
      document.getElementById("captcha").innerHTML = "";
      captchaObj.appendTo("#captcha");
    },

    // 用户登录
    user_login() {
      this.$axios({
        url: this.$settings.HOST + 'user/login/',
        method: 'post',
        data: {
          username: this.username,
          password: this.password,
        }
      }).then(response => {
        console.log(response.data)
        this.$message({
          message: "登录成功",
          type: 'success',
          duration: 2000,
          showClose: true,
        })
        if (this.remember_me) {
          localStorage.setItem('username', this.username)
          localStorage.setItem('password', this.password)
        } else {
          delete localStorage.username
          delete localStorage.password
        }
        localStorage.setItem('token', response.data.token)
        sessionStorage.setItem('token', response.data.token)
        sessionStorage.setItem('username', this.username)
        this.$router.push('/')
      }).catch(error => {
        console.log(error);
        this.$message({
          message: "用户名或密码错误",
          type: 'success',
          duration: 2000,
          showClose: true,
        })
      })
    },
    add1: function () {
      this.user1 = true
      this.user2 = false
    },
    add2: function () {
      this.user1 = false
      this.user2 = true
    }
  }
}
</script>

<style scoped>
.box {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
}

.box img {
  width: 100%;
  min-height: 100%;
}

.box .login {
  position: absolute;
  width: 500px;
  height: 400px;
  top: 0;
  left: 0;
  margin: auto;
  right: 0;
  bottom: 0;
  top: -338px;
}

.login .login-title {
  width: 100%;
  text-align: center;
}

.login-title img {
  width: 190px;
  height: auto;
}

.login-title p {
  font-family: PingFangSC-Regular;
  font-size: 18px;
  color: #fff;
  letter-spacing: .29px;
  padding-top: 10px;
  padding-bottom: 50px;
}

.login_box {
  width: 400px;
  height: auto;
  background: #fff;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, .5);
  border-radius: 4px;
  margin: 0 auto;
  padding-bottom: 40px;
}

.login_box .title {
  font-size: 20px;
  color: #9b9b9b;
  letter-spacing: .32px;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  justify-content: space-around;
  padding: 50px 60px 0 60px;
  margin-bottom: 20px;
  cursor: pointer;
}

.login_box .title span:nth-of-type(1) {
  color: #4a4a4a;
  border-bottom: 2px solid #84cc39;
}

.inp {
  width: 350px;
  margin: 0 auto;
}

.inp input {
  border: 0;
  outline: 0;
  width: 100%;
  height: 45px;
  border-radius: 4px;
  border: 1px solid #d9d9d9;
  text-indent: 20px;
  font-size: 14px;
  background: #fff !important;
}

.inp input.user {
  margin-bottom: 16px;
}

.inp .rember {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  margin-top: 10px;
}

.inp .rember p:first-of-type {
  font-size: 12px;
  color: #4a4a4a;
  letter-spacing: .19px;
  margin-left: 22px;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-align: center;
  align-items: center;
  /*position: relative;*/
}

.inp .rember p:nth-of-type(2) {
  font-size: 14px;
  color: #9b9b9b;
  letter-spacing: .19px;
  cursor: pointer;
}

.inp .rember input {
  outline: 0;
  width: 30px;
  height: 45px;
  border-radius: 4px;
  border: 1px solid #d9d9d9;
  text-indent: 20px;
  font-size: 14px;
  background: #fff !important;
}

.inp .rember p span {
  display: inline-block;
  font-size: 12px;
  width: 100px;
  /*position: absolute;*/
  /*left: 20px;*/

}

#geetest {
  margin-top: 20px;
}

.login_btn {
  width: 100%;
  height: 45px;
  background: #84cc39;
  border-radius: 5px;
  font-size: 16px;
  color: #fff;
  letter-spacing: .26px;
  margin-top: 30px;
}

.inp .go_login {
  text-align: center;
  font-size: 14px;
  color: #9b9b9b;
  letter-spacing: .26px;
  padding-top: 20px;
}

.inp .go_login span {
  color: #84cc39;
  cursor: pointer;
}

.sms-box {
  position: relative;
}

.sms-btn {
  font-size: 14px;
  color: #ffc210;
  letter-spacing: .26px;
  position: absolute;
  right: 16px;
  top: 10px;
  cursor: pointer;
  overflow: hidden;
  background: #fff;
  border-left: 1px solid #484848;
  padding-left: 16px;
  padding-bottom: 4px;
}

</style>