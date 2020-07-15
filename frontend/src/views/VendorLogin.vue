<template>
  <div class="container">

      <h3 class="main-header mt-4" style="text-align: center;">Vendor Login</h3>
      <hr>

        <b-alert class="mt-4 col-md-5 mx-auto" v-model="showAlert" variant="warning" dismissible>
            <strong>{{errorMsg}}</strong>
        </b-alert>


    <form class="text-dark mt-5" @submit.prevent="attemptLogin()">
    
        <div class="form-group" style="text-align: center;">
            <label for="email">Email</label>

            <input required v-model="email" type="email" class="form-control mx-auto col-md-5 col-sm-10" id="email" placeholder="e.g dami@xyz.com">
        </div>


        <div class="form-group" style="text-align: center;">
            <label for="password">Password</label>

            <input required v-model="password" class="form-control mx-auto col-md-5 col-sm-10" id="password" type="password" placeholder="Enter your password here...">
        </div>


        <div class="d-flex justify-content-center mt-5">
                <v-btn type="submit" :loading="loading" :disabled="loading" :color="btnColor" style="color: floralwhite" class="text-capitalize btn btn-block myBtn col-md-5 col-xs-12 col-sm-12">Submit</v-btn>
        </div>

    </form>
      
  </div>
</template>

<script>
export default {
    name: 'VendorLogin',
    data() {
        return {
            email: "",
            password: "",
            errorMsg: null,
            loading: false,
            showAlert: false,
            btnColor: "#162059",
        }
    },
    methods: {
        attemptLogin() {
            let email = this.email;
            let password = this.password;
            this.loading = true

             this.$http.post(`login`, {
                email,
                password
            })
            .then(res => {
                let { user, token } = res.data;
                let data = {user, token}
                this.$store.dispatch('loginUser', data)
                .then(()=> {
                    this.$router.push(this.$route.nextUrl ? this.$route.nextUrl : '/vendors')
                })
                .catch(() => {
                    console.log("Login error")
                })
                
            })
            .catch(err => {
                this.showAlert = true
                this.loading = false
                this.errorMsg = err.response ? err.response.data.error.error[0] : "Error processing your request, please try again"
            })
        }
    }
}
</script>

<style>

</style>