let vm = new Vue({
    el:'#app',
    delimiters:['[[',']]'],
    data:{
        username:'',
        password:'',

        error_username_code:false,
        error_password_code:false,

        error_username_message:'',
        error_password_message:'',
    },
    methods:{
        check_username() {
            let re = /^[a-zA-Z0-9_-]{5,20}$/;
            if(re.test(this.username)){
                this.error_username_code=false;
            }else {
                this.error_username_message='请输入正确的用户名';
                this.error_username_code=true;
            }
        },
        check_password() {
            let re = /^[a-zA-Z0-9]{8,20}$/;
            if(re.test(this.password)){
                this.error_password_code=false;
            }else {
                this.error_password_message='请按要求输入密码';
                this.error_password_code=true;
            }
        },
        check_submit(){
          this.check_password();
          this.check_username();

        },

    },

});