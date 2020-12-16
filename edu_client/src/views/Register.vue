<template>
  <div class="box">
    <img src="../static/image/1111.jpg" alt="">
    <div class="register">
      <div class="register_box">
        <div class="register-title">百知教育在线平台注册</div>
        <div class="inp">
          <input v-model="phone" type="text" placeholder="手机号码" class="user" @blur="check_phone">
          <input v-model="password" type="password" placeholder="登录密码" class="user" @blur="check_password">
          <div id="geetest"></div>
          <div class="sms-box">
            <input v-model="sms_code" type="text" maxlength="6" placeholder="输入验证码" class="user">
            <div class="sms-btn" @click="get_code" id="time">获取验证码<span v-if="disp">-{{ time }}秒</span></div>
          </div>
          <button class="register_btn" @click="user_register">注册</button>
          <p class="go_login">已有账号
            <router-link to="/login">直接登录</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Register",
  data() {
    return {
      phone: '',
      password: '',
      sms_code: '',
      register_flag: false,
      disp: false,
      time: 60
    }
  },
  methods: {
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
    get_code() {
      if (this.register_flag) {
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

    user_register: function () {
      let regg = /^(?![d]+$)(?![a-zA-Z]+$)(?![^da-zA-Z]+$).{6,18}$/;
      if (this.phone === '' || this.password === '' || this.sms_code === '') {
        this.$message({
          message: "账号或密码或验证码不能为空",
          type: 'success',
          duration: 2000,
          showClose: true,
        })
      } else if (this.register_flag) {
        this.$axios({
          url: this.$settings.HOST + "user/register/",
          method: "post",
          data: {
            phone: this.phone,
            password: this.password,
            sms_code: this.sms_code,
          },
        }).then(response => {
          console.log(response);
          // 保存用户信息  自动登录
          localStorage.setItem('username', this.phone)
          sessionStorage.setItem('username', this.phone)
          localStorage.setItem('token', response.data.data.token)
          sessionStorage.setItem('token', response.data.data.token)
          let self = this;
          this.$alert("注册成功", "百知教育", {
            callback() {
              self.$router.push("/")
            }
          })
        }).catch(error => {
          console.log(error);
          this.$message({
            message: '注册失败',
            type: 'success',
            duration: 2000,
            showClose: true,
          })
        })
      }
    },


    check_password() {
      let reg = /^(?![\d]+$)(?![a-zA-Z]+$)(?![^\da-zA-Z]+$).{6,18}$/;
      if (this.password === '') {
        this.$message({
          message: "密码不能为空",
          type: 'success',
          duration: 2000,
          showClose: true,
        })
      }
      else if (!reg.test(this.password)) { // 前端检测手机号长度是否符合要求
        this.$message({
          message: "密码格式为6-18位，数字/字母/特殊字符任意两种组合",
          type: 'success',
          duration: 2000,
          showClose: true,
        })
      } else {
        this.register_flag = true
      }
    },

    // 检查手机号是否唯一
    check_phone() {
      let reg = /^1[3-9]\d{9}$/;
      if (this.phone === '') {
        this.$message({
          message: "手机不能为空",
          type: 'success',
          duration: 2000,
          showClose: true,
        })
      } else if (!reg.test(this.phone)) { // 前端检测手机号长度是否符合要求
        this.$message({
          message: "手机号格式不正确",
          type: 'success',
          duration: 2000,
          showClose: true,
        })
      }
      this.$axios({
        url: this.$settings.HOST + "user/phone/",
        method: 'post',
        data: {
          phone: this.phone
        }
      }).then(response => {
        console.log(response)
        this.register_flag = true
        sessionStorage.setItem('username',this.phone)
      }).catch(onerror => {
        this.$message({
          message: "手机号已被注册",
          type: 'success',
          duration: 2000,
          showClose: true,
        })
      })
    }
  },
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

.box .register {
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

.register .register-title {
  width: 100%;
  font-size: 24px;
  text-align: center;
  padding-top: 30px;
  padding-bottom: 30px;
  color: #4a4a4a;
  letter-spacing: .39px;
}

.register-title img {
  width: 190px;
  height: auto;
}

.register-title p {
  font-family: PingFangSC-Regular;
  font-size: 18px;
  color: #fff;
  letter-spacing: .29px;
  padding-top: 10px;
  padding-bottom: 50px;
}

.register_box {
  width: 400px;
  height: auto;
  background: #fff;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, .5);
  border-radius: 4px;
  margin: 0 auto;
  padding-bottom: 40px;
}

.register_box .title {
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

.register_box .title span:nth-of-type(1) {
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

.register_btn {
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