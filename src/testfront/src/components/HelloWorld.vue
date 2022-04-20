<template>
  <q-page class="flex flex-center">
    
    <div class="q-pa-md" style="max-width: 400px">
    
    <q-btn label="Войти" color="primary" v-if="!user" @click="login" />
    <div v-if="user"> {{ greeting }} </div>
    <div v-if="user"> {{ userStatus }} </div>

    <q-form
      @submit="onSubmit"
      @reset="onReset"
      class="q-gutter-md"
      v-if="user"
    >
      <h4>{{ motivation }}</h4>
      <q-input
        filled
        type="number"
        v-model="monthCount"
        label="Количество месяцев"
        lazy-rules
        :rules="[
          val => val !== null && val !== '' || 'Please type month count'
        ]"
      />

      <div>
        <q-btn label="Купить" type="submit" color="primary" :disabled="!user"/>
      </div>
    </q-form>

    {{ history }}
  </div>

  </q-page>
</template>

<style>
</style>

<script setup>
import { ref } from 'vue'
import jwt_decode from "jwt-decode"
// import { openURL } from 'quasar'

const monthCount=ref(3);
const history=ref();
const greeting=ref();
const userStatus=ref();
const motivation=ref("Купить подписку");


const user=ref();

function login() {
  fetch('http://127.0.0.1/api/v1/auth/user/login/', {
    method: 'POST',
    body: JSON.stringify({"password": "tochange", "username": "alisovenko"}),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    console.log(data.access_token);
    user.value = data.access_token

    var decoded = jwt_decode(user.value);
    console.log(decoded);


    greeting.value = 'Hello, ' + decoded.sub + '!'

    if ('vip' in decoded){
      userStatus.value = ' You are VIP! )'
      motivation.value = 'Продли подписку'
    }else{
      userStatus.value = ' You are not VIP ('      
      motivation.value = 'Купи подписку'
    }
  });
}

function onSubmit() {
  fetch('http://127.0.0.1/api/v1/payment/', {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer ' + user.value
    },
    body: JSON.stringify({"product_id": "8b14aa60-6b09-4ced-a344-aca486419592"}),
  })
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    console.log(data);
    
    // openURL(
    //   data,
    //   'paymentWindow',
    //   // 'popup=true'
    //   {
    //     popup: true,
    //     // scrollbars: false,
    //     // resizable: false,
    //     // status: false,
    //     // location: false,
    //     // toolbar: false,
    //     // menubar: false,   
    //     width: 600,
    //     height: 300,
    //     left: 100,
    //     top: 100
    //   }
    // )
    let windowFeatures = "left=100,top=100,width=1200,height=640";

    window.open(data, "payWindow", windowFeatures);
    // window.open(data, '_blank').focus();
    // history.value = data;
  });

}

</script>
