let vm = new Vue({
    el: '#reg_app',
    delimiters: ['[[',']]'],
    data:{
        username:'',
        password:'',
        password2:'',

        image_code_url:'',
        uuid:'',
        img_code:'',

        send_flag:false,

        error_name:false,
        error_password:false,
        error_password2:false,

        err_img_code:false,


        error_name_message:'',
        err_img_code_msg:'',

    },
    mounted(){
        this.generate_image_code();

    },
    methods:{
        send_sms_code(){
            if (this.send_flag == true){
                return;
            }
            this.send_flag = true;
            this.check_mobile();
            this.check_img_code();
            if(this.error_mobile==true||this.err_img_code==true){
                this.send_flag=false;
                return;
            }
            let url = '/sms_codes/'+this.mobile+'/?img_code='+this.img_code+'&uuid='+this.uuid;
            axios.get(url,{
                responseType: 'json'
            })
                .then(response => {
                    if(response.data.code == '0'){
                        let num = 60;
                        let t = setInterval(()=>{
                            if (num == 1){
                                clearInterval(t);
                                this.sms_code_msg = '获取短信验证码';
                                this.generate_image_code();
                                this.send_flag=false;
                            }else {
                                num -= 1;
                                this.sms_code_msg = num + '秒';
                            }

                        },1000)

                    }else {
                        if(response.data.code == '4001'){
                            this.err_img_code_msg = response.data.errmsg;
                            this.err_img_code = true;
                            this.send_flag=false;

                        }
                    }

                })
                .catch(response =>{
                    console.log(error.response);
                    this.send_flag=false;

                })

        },
        generate_image_code(){
            this.uuid=guid();
            this.image_code_url='/image_codes/'+this.uuid+'/';
        },
        check_username(){
            let re = /^[a-zA-Z0-9_-]{5,20}$/;
            if (re.test(this.username)){
                this.error_name = false;
            }else {
                this.error_name_message = '请输入5-20位用户名';
                this.error_name = true;
            }
            if(this.error_name==false){
                let url = '/usernames/'+this.username+'/count/';
                axios.get(url,{
                    responseType:'json'
                })
                    .then(response=>{
                        if(response.data.count==1){
                            this.error_name_message = '用户名已存在';
                            this.error_name=true;
                        }else {
                            this.error_name=false;
                        }

                    })
                    .catch(error=>{
                        console.log(error.response);
                    })
            }

        },
        check_password(){
            let re = /^[a-zA-Z0-9]{8,20}$/;
            if (re.test(this.password)){
                this.error_password=false;
            }else {
                this.error_password=true;
            }

        },
        check_password2(){
            if (this.password2 == this.password){
                this.error_password2=false;
            }else {
                this.error_password2=true;
            }

        },
        check_img_code(){
            if(this.img_code.length != 4){
                this.err_img_code_msg = '请输入验证码';
                this.err_img_code = true;

            }else {
                this.err_img_code = false;

            }
        },
        check_mobile(){


        },
        on_submit(){

        }

        }
});