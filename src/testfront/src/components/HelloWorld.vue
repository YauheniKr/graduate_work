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

    if (decoded.subscribe_expired){
      userStatus.value = ' У вас уже есть подписка до ' + decoded.subscribe_expired
      motivation.value = 'Продли подписку'
    }else{
      userStatus.value = ' У вас нет подписки'      
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
    body: JSON.stringify(
      {
        "product_id": "8b14aa60-6b09-4ced-a344-aca486419592",
        "success_url": "http://localhost:8080/",
        "cancel_url": "http://localhost:8080/"
      }
    ),
  })
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    console.log(data);
    window.open(data, "_self");
  });

}

</script>
