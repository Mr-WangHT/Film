<template>
    <div>
        <div class="movies">
            <div class="card_x" v-for="movie in movie_list">
                <b-card
                        v-bind:title="movie.name"
                        v-bind:img-src="movie.poster"
                        img-alt="Image"
                        img-top
                        tag="article"
                        style="max-width: 20rem;"
                        class="mb-2"
                >
                    <b-card-text>
                        {{movie.info}}
                    </b-card-text>

                    <b-button href="#" variant="primary">Go somewhere</b-button>
                </b-card>
            </div>
        </div>
    </div>

</template>

<script>
    export default {
        name: "HomePage",
        data() {
            return {
                movie_list: []
            }
        },
        mounted() {
            this.showMoviesFromDRF();
        },
        methods: {

            showMoviesFromDRF() {
                const obj = this;
                const url = "http://127.0.0.1:8000/movie/api/movie";
                this.$http.get(url,{
                    params:{
                        token:'7ce0b76ac67fe23d87b68565a6258d62'
                    }
                }).then(
                    (response) => {
                        obj.movie_list = JSON.parse(response.request.response);
                    }
                )
            },
        }
    }
</script>

<style scoped>

    .movies {
        margin-top: 20px;
        float: left;
    }

    .card_x {
        float: left;
        margin: 10px;
    }

</style>
