<template>
  <footer class="footer text-center">
    <div class="container p-3">
      <span class="text-muted">&copy; {{date}} <a class="blueColor" href="http://jesutomiwa.me">Jesutomiwa Salam</a>, All Rights Reserved. </span>
    </div>
  </footer>
</template>

<script>
export default {
    name: "Footer",
    data () {
        return {
            date: new Date().getFullYear()
        }
    }
}
</script>

<style>

</style>