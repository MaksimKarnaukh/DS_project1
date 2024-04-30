<script setup lang="ts">
import {ref} from "vue";
import type {Ref} from "vue";
import axios from "axios"

const firstXMovies = ref(0); // amount of popular movies to show (represents the user input)

const selectedMovie = ref(-1);

// table info
const tableHeaders: Array<string> = ["Movie Name", "Popularity", "Delete", "Like"];
const movieList: Ref<Array<any>> = ref([]);
const movieListSimilarGenres: Ref<Array<any>> = ref([]);
const movieListSimilarRuntime: Ref<Array<any>> = ref([]);
const movieListSimilarActors: Ref<Array<any>> = ref([]);

// fetches
const response_err = ref(false);
/**
 * getPopularMovies: 
 */
async function getPopularMovies() {
  try {
    const API_BASE_URL = 'http://127.0.0.1:5000'; // window.location.origin;
    const response = await axios.get(`${API_BASE_URL}/movies/popular?amount=${firstXMovies.value}`);
    console.log(response);
    movieList.value = response.data["movies"];
    response_err.value = false;
  } catch (error) {
    response_err.value = true;
    console.log(error);
  }
}

async function getRecommendations(movie_id: number) {
  try {
    const API_BASE_URL = 'http://127.0.0.1:5000'; // window.location.origin;
    const response_similar_genres = await axios.get(`${API_BASE_URL}/movies/${movie_id}/similar-genres`);
    const response_similar_runtime = await axios.get(`${API_BASE_URL}/movies/${movie_id}/similar-runtime`);
    const response_similar_actors = await axios.get(`${API_BASE_URL}/movies/${movie_id}/similar-actors`);

    console.log(response_similar_genres.data);
    console.log(response_similar_runtime.data);
    console.log(response_similar_actors.data);
    movieListSimilarGenres.value = response_similar_genres.data["movies"];
    movieListSimilarRuntime.value = response_similar_runtime.data["movies"];
    movieListSimilarActors.value = response_similar_actors.data["movies"];
    selectedMovie.value = movie_id;

    response_err.value = false;
  } catch (error) {
    response_err.value = true;
    console.log(error);
  }
}

async function deleteMovie(movie_id: number) {
  try {
    const API_BASE_URL = 'http://127.0.0.1:5000'; // window.location.origin;
    const response = await axios.delete(`${API_BASE_URL}/movies/${movie_id}`);
    console.log(response.data);
    getPopularMovies();
    if (selectedMovie.value !== -1) {
      getRecommendations(selectedMovie.value);
    }
    response_err.value = false;
  } catch (error) {
    response_err.value = true;
    console.log(error);
  }
}

async function likeMovie(movie_id: number) {
  try {
    const API_BASE_URL = 'http://127.0.0.1:5000'; // window.location.origin;
    const response = await axios.put(`${API_BASE_URL}/movies/${movie_id}`);
    console.log(response.data);
    getPopularMovies();
    if (selectedMovie.value !== -1) {
      getRecommendations(selectedMovie.value);
    }
    response_err.value = false;
  } catch (error) {
    response_err.value = true;
    console.log(error);
  }
}

async function generateBarplot() {
  try {
    const API_BASE_URL = 'http://127.0.0.1:5000'; // window.location.origin;
    let movie_ids = movieList.value.map((movie) => movie.id).join(",");
    console.log(movie_ids);
    const response = await axios.get(`${API_BASE_URL}/movies/barplot?movie-ids=${movie_ids}`);
    console.log(response.data);
    let chart_url = response.data["chart_url"];
    chart_url.replaceAll('\"', '"')
    window.open(chart_url, '_blank');
    response_err.value = false;
  } catch (error) {
    response_err.value = true;
    console.log(error);
  }
}

</script>

<template>
  <main class="container text-white">
    <div class="pt-12 mb-8 relative text-center">
      <input type="text" v-model.number="firstXMovies" placeholder="List the amount of movies to show" class="py-2 px-1 w-1/4 bg-transparent border-b focus:border-g-a2 focus:outline-none focus:shadow-[0px_1px_0_0_#000000]">
      <button @click="getPopularMovies" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded ml-4">Show</button>
    </div>

    <div class="w-[75%] relative overflow-x-auto mt-12 overflow-y-auto h-96 mx-auto">
      <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400 dark:bg-gray-700">
        <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:text-gray-400 top-0">
          <tr>
            <th scope="col" v-for="(item, index) in tableHeaders" :key="index" class="px-6 py-3 text-center sticky dark:bg-gray-700 top-0">
                {{ item }}
            </th>
          </tr>
        </thead>
        <tbody class="">
          <tr v-for="(item, index) in movieList" :key="index" class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 text-center">
            <th scope="row" class="px-6 py-4 cursor-pointer font-medium text-gray-900 whitespace-nowrap dark:text-white" @click="getRecommendations(item.id)">
              {{ item.name }}
            </th>
            <td class="px-6 py-4">
              {{ item.pop }}
            </td>
            <td class="px-6 py-4">
              <svg class="inline h-6 w-6 cursor-pointer text-red-600 ease-in hover:-translate-y-0.5 active:translate-y-0" @click="deleteMovie(item.id)" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
            </td>
            <td v-if="item.liked" class="px-6 py-4">
              <i class="fa-solid fa-heart cursor-pointer text-green-600 ease-in hover:-translate-y-0.5 active:translate-y-0" @click="likeMovie(item.id)"></i>
            </td>
            <td v-else class="px-6 py-4">
              <i class="fa-regular fa-heart cursor-pointer text-green-600 ease-in hover:-translate-y-0.5 active:translate-y-0" @click="likeMovie(item.id)"></i>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="text-center mt-12">
      <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" @click="generateBarplot()">
        Generate Barplot
      </button>
    </div>

    <!-- 3 tables: similar genres, similar runtime and similar actors -->

    <div class="grid grid-cols-3 gap-6" v-if="selectedMovie !== -1">

      <div class="mt-12">
        <p class="text-center">Similar Genres</p>
        <div class="overflow-x-auto mt-6 overflow-y-auto h-96">
          <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400 dark:bg-gray-700">
            <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:text-gray-400 top-0">
              <tr>
                <th scope="col" v-for="(item, index) in tableHeaders" :key="index" class="px-6 py-3 text-center sticky dark:bg-gray-700 top-0">
                    {{ item }}
                </th>
              </tr>
            </thead>
            <tbody class="">
              <tr v-for="(item, index) in movieListSimilarGenres" :key="index" class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 text-center">
                <th scope="row" class="px-6 py-4 cursor-pointer font-medium text-gray-900 whitespace-nowrap dark:text-white" @click="getRecommendations(item.id)">
                  {{ item.name }}
                </th>
                <td class="px-6 py-4">
                  {{ item.pop }}
                </td>
                <td class="px-6 py-4">
                  <svg class="inline h-6 w-6 cursor-pointer text-red-600 ease-in hover:-translate-y-0.5 active:translate-y-0" @click="deleteMovie(item.id)" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                </td>
                <td v-if="item.liked" class="px-6 py-4">
                  <i class="fa-solid fa-heart cursor-pointer text-green-600 ease-in hover:-translate-y-0.5 active:translate-y-0" @click="likeMovie(item.id)"></i>
                </td>
                <td v-else class="px-6 py-4">
                  <i class="fa-regular fa-heart cursor-pointer text-green-600 ease-in hover:-translate-y-0.5 active:translate-y-0" @click="likeMovie(item.id)"></i>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="mt-12">
        <p class="text-center">Similar Runtime</p>
        <div class="overflow-x-auto mt-6 overflow-y-auto h-96">
          <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400 dark:bg-gray-700">
            <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:text-gray-400 top-0">
              <tr>
                <th scope="col" v-for="(item, index) in tableHeaders" :key="index" class="px-6 py-3 text-center sticky dark:bg-gray-700 top-0">
                    {{ item }}
                </th>
              </tr>
            </thead>
            <tbody class="">
              <tr v-for="(item, index) in movieListSimilarRuntime" :key="index" class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 text-center">
                <th scope="row" class="px-6 py-4 cursor-pointer font-medium text-gray-900 whitespace-nowrap dark:text-white" @click="getRecommendations(item.id)">
                  {{ item.name }}
                </th>
                <td class="px-6 py-4">
                  {{ item.pop }}
                </td>
                <td class="px-6 py-4">
                  <svg class="inline h-6 w-6 cursor-pointer text-red-600 ease-in hover:-translate-y-0.5 active:translate-y-0" @click="deleteMovie(item.id)" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                </td>
                <td v-if="item.liked" class="px-6 py-4">
                  <i class="fa-solid fa-heart cursor-pointer text-green-600 ease-in hover:-translate-y-0.5 active:translate-y-0" @click="likeMovie(item.id)"></i>
                </td>
                <td v-else class="px-6 py-4">
                  <i class="fa-regular fa-heart cursor-pointer text-green-600 ease-in hover:-translate-y-0.5 active:translate-y-0" @click="likeMovie(item.id)"></i>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="mt-12">
        <p class="text-center">Similar Actors</p>
        <div class="overflow-x-auto mt-6 overflow-y-auto h-96">
          <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400 dark:bg-gray-700">
            <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:text-gray-400 top-0">
              <tr>
                <th scope="col" v-for="(item, index) in tableHeaders" :key="index" class="px-6 py-3 text-center sticky dark:bg-gray-700 top-0">
                    {{ item }}
                </th>
              </tr>
            </thead>
            <tbody class="">
              <tr v-for="(item, index) in movieListSimilarActors" :key="index" class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 text-center">
                <th scope="row" class="px-6 py-4 cursor-pointer font-medium text-gray-900 whitespace-nowrap dark:text-white" @click="getRecommendations(item.id)">
                  {{ item.name }}
                </th>
                <td class="px-6 py-4">
                  {{ item.pop }}
                </td>
                <td class="px-6 py-4">
                  <svg class="inline h-6 w-6 cursor-pointer text-red-600 ease-in hover:-translate-y-0.5 active:translate-y-0" @click="deleteMovie(item.id)" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                </td>
                <td v-if="item.liked" class="px-6 py-4">
                  <i class="fa-solid fa-heart cursor-pointer text-green-600 ease-in hover:-translate-y-0.5 active:translate-y-0" @click="likeMovie(item.id)"></i>
                </td>
                <td v-else class="px-6 py-4">
                  <i class="fa-regular fa-heart cursor-pointer text-green-600 ease-in hover:-translate-y-0.5 active:translate-y-0" @click="likeMovie(item.id)"></i>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>

  </main>
</template>
