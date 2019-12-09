<template>
  <v-container>
    <v-layout
      text-center
      wrap
    >
      <v-flex xs12>
        <v-img
          :src="require('../assets/archarrow.png')"
          class="my-3"
          contain
          height="200"
        ></v-img>
      </v-flex>

      <v-flex mb-4>
        <h1 class="display-2 font-weight-bold mb-3">
          Welcome to Arch[scor]er
        </h1>
        <p class="subheading font-weight-regular">
          Create, score and archive archery events. The site is work in progress.
          The main functionality can be found under 'events' page where you can
          create new events - for personal training sessions, have fun with club
          as well conduct official competitions.
        </p>
      </v-flex>

      <v-flex
        mb-5
        xs12
      >
        <h2 class="headline font-weight-bold mb-3">What's next?</h2>

        <p>
          First it might be good idea to create user account by either logging in
          with your Google account or create local account. Then try the site out
          on a training session. Then please give feedback -- there is no feedback
          page yet, but most of you should know how to reach me :)
        </p>
      </v-flex>

      <v-flex
        xs12
        mb-5
      >
        <h2 class="headline font-weight-bold mb-3">Important</h2>

        <p colour="alert">
          As we are in the testing phase, I wont guarantee that your events and
          scores can be safely propagated to the future instances, but I'll give
          my best not to lose them either.
        </p>
      </v-flex>

    </v-layout>
  </v-container>
</template>

<script>
  export default {
    data: () => ({
      //
    })
  }
</script>
