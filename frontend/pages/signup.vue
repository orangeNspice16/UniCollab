<template>
<div>
  <v-row><div class="frame mt-10"></div></v-row>
  <v-row>
    <div style="height: 10px"></div>
    <v-col cols="1" class="vertical-frame"></v-col>
    <v-col cols="10" class="content">
      <v-row justify="center" class="mt-10"><div class="title-text">sign up</div></v-row>
      <v-row class="ml-6 mr-6 mt-10">
        <v-text-field placeholder="First Name" label="First Name" outlined></v-text-field>
        <v-spacer></v-spacer>
        <v-text-field placeholder="Last Name" label="Last Name" outlined></v-text-field>
      </v-row>
      <v-row class="ml-6 mr-6 mt-5">
        <v-text-field placeholder="Email" label="Email" outlined></v-text-field>
        <v-spacer></v-spacer>
        <v-text-field placeholder="University" label="University" outlined></v-text-field>
      </v-row>
      <v-row class="ml-6 mr-6 mt-5">
        <v-text-field
            :value="userPassword"
            label="Password"
            placeholder="Password"
            :append-icon="value ? 'mdi-eye-off' : 'mdi-eye'"
            @click:append="() => (value = !value)"
            :type="value ? 'password' : 'text'"
            outlined
        ></v-text-field>
        <v-spacer></v-spacer>
        <v-text-field
            :value1="userPassword"
            label="Confirm Password"
            placeholder="Confirm Password"
            :append-icon="value1 ? 'mdi-eye-off' : 'mdi-eye'"
            @click:append="() => (value1 = !value1)"
            :type="value1 ? 'password' : 'text'"
            outlined
        ></v-text-field>
      </v-row>
      <v-row justify="center" class="mt-10">
        <v-btn color="#55CBD3" dark elevation="0" @click="signup">
          Sign Up
        </v-btn>
        <v-btn @click="$router.push(`/`)" color="#55CBD3" dark elevation="0" class="ml-10">
          Cancel
        </v-btn>
      </v-row>
    </v-col>
    <v-col cols="1.25" class="vertical-frame"></v-col>
  </v-row>
  <v-row><div class="bottom-frame"></div></v-row>
</div>
</template>

<script>
export default {
  data: () => ({
    userPassword: "",
    valid: true,
    value: true,
    value1: true,
  }),
  methods: {
    signup(){
      this.$router.push(`/user/1`)
    }
  },
  // data: () => ({
  //   windowSize: {
  //     x: 0,
  //     y: 0
  //   }
  // }),

  // mounted () {
  //   this.onResize()
  // },

  // methods: {
  //   onResize () {
  //     this.windowSize = { x: window.innerWidth, y: window.innerHeight }
  //   }
  // }
}
</script>

<style scoped lang="scss">
.frame{
  top: 50%;
  height: 70px;
  width: 100%;
  background-color: #93E8EE
}
.vertical-frame{
  height: 600px;
  width: 100%;
  background-color: #93E8EE
}
.bottom-frame{
  height: 70px;
  width: 100%;
  background-color: #93E8EE;
}
.content{
  background-color: white;
  .title-text{
    color: #55CBD3;
    font-size: 40px;
    font-weight: bold;
  }
}
</style>