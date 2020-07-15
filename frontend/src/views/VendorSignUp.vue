<template>
  <div class="container">

      <h3 class="main-header mt-4" style="text-align: center;">Become A Vendor</h3>
      <hr>

        <b-alert class="mt-4 col-md-5 mx-auto" v-model="showAlert" variant="warning" dismissible>
            <strong>{{errorMsg}}</strong>
        </b-alert>


    <form class="text-dark mt-5" @submit.prevent="attemptSignUp()">

        <div class="form-group" style="text-align: center;">
            <label for="email">Surname</label>

            <input required v-model="last_name" type="text" class="form-control mx-auto col-md-5 col-sm-10" id="last_name" placeholder="Enter your surname here...">
        </div>

        <div class="form-group" style="text-align: center;">
            <label for="first_name">Firstname</label>

            <input required v-model="first_name" type="text" class="form-control mx-auto col-md-5 col-sm-10" id="first_name" placeholder="Enter your firstname here...">
        </div>

    
        <div class="form-group" style="text-align: center;">
            <label for="email">Email</label>

            <input required v-model="email" type="email" class="form-control mx-auto col-md-5 col-sm-10" id="email" placeholder="e.g dami@xyz.com">
        </div>

        <b-form-group label-for="state_of_residence" class="mx-auto col-md-5 col-sm-10">
            <template v-slot:label>
                State Of Residence
            </template>
            <b-form-select required v-model="state_of_residence">
                <b-form-select-option :value="state" v-for="state in states" :key="state">{{state}}</b-form-select-option>
            </b-form-select>
        </b-form-group>


        <div class="form-group" style="text-align: center;">
            <label for="password">Password</label>

            <input required v-model="password" class="form-control mx-auto col-md-5 col-sm-10" id="password" type="password" placeholder="Enter your password here...">
        </div>

        <b-form-group label-for="conf_password">
            <template v-slot:label>
                Confirm Password <span class="text-danger">*</span>
            </template>
            <b-form-input :disabled="!password" id="conf_password" class="form-control mx-auto col-md-5 col-sm-10" v-model="conf_password" type="password" required placeholder="Confirm Password"></b-form-input>
        </b-form-group>


        <div class="d-flex justify-content-center mt-5">
                <v-btn type="submit" :loading="loading" :disabled="loading || (password && password !== conf_password)" :color="btnColor" style="color: floralwhite" class="text-capitalize btn btn-block myBtn col-md-5 col-xs-12 col-sm-12">Sign Up</v-btn>
        </div>

    </form>
      
  </div>
</template>

<script>
import states from '@/helpers/states.js'

export default {
    name: 'VendorSignUp',
    data() {
        return {
            first_name: "",
            last_name: "",
            email: "",
            password: "",
            conf_password: "",
            state_of_residence: "",
            states: states,
            errorMsg: null,
            loading: false,
            showAlert: false,
            btnColor: "#162059",
        }
    },
    methods: {
        attemptSignUp() {
            let { first_name, last_name, email, password, state_of_residence } = this
            this.loading = true

             this.$http.post(`signup`, {
                first_name,
                last_name,
                state_of_residence,
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
                this.errorMsg = err.response ? err.response.data.error.email[0] : "Error processing your request, please try again"
            })
        },
    }
}
</script>

<style>

</style>