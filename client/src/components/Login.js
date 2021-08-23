const  Login = {
    data: function() { 
        return {
            server: 'http://127.0.0.1:8000',
            username: '',
            password: '',
            error: '',
        }
    },
    methods: {
        login: function(event) {
            event.preventDefault();
            if(this.username && this.password) {
                this.$store.dispatch('login', {
                    server: this.server,
                    username: this.username,
                    password: this.password
                }).then(() => {
                    this.$router.push('/');
                }
                ).catch(error => {
                    this.error = "Cannot login";
                });
            }
            return false;
        }
    },
    template: `
    
<h3>Login</h3>
<form class='login' method="post" action="" >
    <div class="mb-3 mt-3">
      <label class='control-label'>Server</label>
      <input type='text' class='form-control' name='server' v-model='server' required>
    </div>
    <div class="mb-3 mt-3">
      <label class='control-label'>Username</label>
      <input type='text' class='form-control' name='username' v-model='username' required>
    </div>
  
    <div class="mb-3">
      <label class='control-label'>Password</label>
      <input type='password' class='form-control' name='password' v-model='password' required>
      
    </div>
    <div class='alert alert-danger' v-if='error'>
        {{ error }}
    </div>
    <button class='btn btn-outline-info btn-sm' @click='login'>Login</button>
    
</form>
  
    `
}

export default Login