<template>
  <q-page class="flex flex-center">
    
    <div class="q-pa-md" style="max-width: 400px">
    <h4>Купи подписку</h4>
    <q-form
      @submit="onSubmit"
      @reset="onReset"
      class="q-gutter-md"
    >
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
        <q-btn label="Купить" type="submit" color="primary"/>
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


const monthCount=ref(3);
const history=ref();

function onSubmit() {
  console.log('Купить ' + monthCount.value + ' месяца(ев) подписки')

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

    fetch('http://127.0.0.1/api/v1/auth/user/history/?limit=10&page=1', {
      method: 'GET',
      headers: {
        'Authorization': 'Bearer ' + data.access_token
      }
    })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log(data);
      history.value = data;
    });

  });
}

</script>
