<template>
  <v-dialog v-model="dialog" persistent max-width="400px">
    <template v-slot:activator="{ on }">
      <v-btn text v-on="on">login</v-btn>
    </template>
    <v-form method="POST" action="/accounts/login/">
      <v-card class="px-6">
        <v-card-title class="justify-center">
          Login
        </v-card-title>
        <v-card-text>
          <a title="Google"
            :href="'/accounts/google/login/?process=login&amp;next=/%23' + $route.path">
            <div class="google"></div>
          </a>
          <v-divider />

          <v-text-field
            label="Login"
            name="login"
            prepend-icon="mdi-account"
            type="text"
          />

          <v-text-field
            id="password"
            label="Password"
            name="password"
            prepend-icon="mdi-lock"
            type="password"
          />
          <!-- this is needed for security reasons -->
          <input type="hidden" name="csrfmiddlewaretoken"
            :value="csrf" />
          <input type="hidden" name="next"
            :value="'/#' + $route.path" />
          <p>If you have not created an account yet, then please
          <a :href="'accounts/signup/?next=/%23' + $route.path">sign up</a> first.</p>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="dialog = false">Close</v-btn>
          <v-btn color="primary" type="submit">Login</v-btn>
        </v-card-actions>
      </v-card>
    </v-form>
  </v-dialog>
</template>

<script>

  export default {
    props: {
      csrf: String,
    },
    data: () => ({
      dialog: false,
    }),
  }
</script>

<style scoped>
  .google {
    background: url('~@/assets/btn_google_signin_dark_normal_web@2x.png') no-repeat center center;
    background-size: contain;
    width: 198px;
    height: 47px;
    margin: 30px auto;
    padding: 0px 0px;
    overflow: hidden;
  }
</style>
