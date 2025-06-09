<script setup>
import { ref } from 'vue'
import axios from 'axios'

const tasks = ref([
  { task_name: '', time_mode: '2', hours: null, minutes: null, start: '', end: '' }
])

const summary = ref(null)

function addTask() {
  tasks.value.push({ task_name: '', time_mode: '2', hours: null, minutes: null, start: '', end: '' })
}

function removeTask(index) {
  tasks.value.splice(index, 1)
}

async function submitTasks() {
  try {
    // Clean data: remove unused fields based on time_mode
    const cleanTasks = tasks.value.map(task => {
      if (task.time_mode === '1') {
        return {
          task_name: task.task_name,
          time_mode: task.time_mode,
          start: task.start,
          end: task.end
        }
      } else {
        return {
          task_name: task.task_name,
          time_mode: task.time_mode,
          hours: task.hours,
          minutes: task.minutes
        }
      }
    })

    const response = await axios.post('https://daily-planner-1.onrender.com/process-tasks', cleanTasks)
    // const response = await axios.post('http://127.0.0.1:8000/process-tasks', cleanTasks)

    summary.value = response.data
  } catch (error) {
    console.error("Error:", error)
  }
}
</script>

<template>
  <div class="p-4 max-w-xl mx-auto">
    <h1 class="text-xl font-bold mb-4">Daily Task Planner</h1>
    <div v-for="(task, index) in tasks" :key="index" class="task-card">
      <label>
        Task Name:
        <input v-model="task.task_name" type="text" class="w-full"/>
      </label>

      <label class="block mt-2">
        Time Mode:
        <select v-model="task.time_mode" class="border p-1 rounded">
          <option value="2">Hours/Minutes</option>
          <option value="1">Start/End Time</option>
        </select>
      </label>

      <div v-if="task.time_mode === '2'" class="flex gap-2 mt-2">
        <label>Hours: <input v-model="task.hours" type="number" class="border p-1 rounded w-20" /></label>
        <label>Minutes: <input v-model="task.minutes" type="number" class="border p-1 rounded w-20" /></label>
      </div>

      <div v-else class="flex gap-2 mt-2">
        <label>Start: <input v-model="task.start" type="text" placeholder="HH:MM" class="border p-1 rounded w-20" /></label>
        <label>End: <input v-model="task.end" type="text" placeholder="HH:MM" class="border p-1 rounded w-20" /></label>
      </div>

      <button @click="removeTask(index)" class="mt-2 text-red-500 text-sm">Remove Task</button>
    </div>

    <button @click="addTask" class="bg-blue-500 text-white px-3 py-1 rounded">Add Task</button>
    <button @click="submitTasks" class="bg-green-500 text-white px-3 py-1 rounded ml-2">Submit Tasks</button>

    <div v-if="summary" class="summary-box">
      <h2 class="font-bold">Summary:</h2>
      <p>Total hours: {{ summary.total_hours }}</p>
      <ol>
        <li v-for="task in summary.tasks" :key="task.task_name">
          {{ task.task_name }} - {{ task.duration_hours }} hours
        </li>
      </ol>
    </div>
  </div>
</template>
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

body {
  font-family: 'Press Start 2P', monospace;
  background-color: #e0e0d0;
  color: #000;
  padding: 2rem;
  image-rendering: pixelated;
}

h1 {
  font-size: 12px;
  text-align: center;
  color: #000;
  text-transform: uppercase;
  line-height: 1.4;
  margin-bottom: 2rem;
  text-shadow: 1px 1px 0 #ccc;
}

.p-4 {
  background-color: #f0f0e0;
  border: 4px solid #444;
  padding: 2rem;
  max-width: 320px;
  margin: 0 auto;
  box-shadow: inset -2px -2px 0 #999;
}

label {
  font-size: 10px;
  display: block;
  margin-bottom: 0.5rem;
}

input,
select {
  padding: 0.4rem;
  font-family: 'Press Start 2P', monospace;
  font-size: 10px;
  background-color: #f8f8f0;
  border: 2px solid #555;
  color: #000;
  margin-bottom: 1rem;
  box-shadow: inset 2px 2px 0 #aaa;
  image-rendering: pixelated;
}

button {
  font-family: 'Press Start 2P', monospace;
  font-size: 10px;
  padding: 0.6rem 1rem;
  border: 2px solid #000;
  cursor: pointer;
  margin-top: 0.5rem;
  margin-right: 0.5rem;
  image-rendering: pixelated;
  box-shadow: 3px 3px 0 #000;
}

button:hover {
  opacity: 0.9;
}

.bg-blue-500 {
  background-color: #4a90e2;
  color: white;
}

.bg-green-500 {
  background-color: #7ed957;
  color: black;
}

.summary-box {
  border: 2px solid #000;
  background-color: #e0e0d0;
  padding: 1rem;
  font-size: 10px;
  margin-top: 1.5rem;
  box-shadow: inset 2px 2px 0 #aaa;
}

.task-card {
  background-color: #e0e0d0;
  border: 3px dashed #555;
  box-shadow: 4px 4px 0 #000;
  padding: 1rem;
  margin-bottom: 1.5rem;
}
</style>


