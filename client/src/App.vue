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

    const response = await axios.post('http://127.0.0.1:8000/process-tasks', cleanTasks)
    summary.value = response.data
  } catch (error) {
    console.error("Error:", error)
  }
}
</script>

<template>
  <div class="p-4 max-w-xl mx-auto">
    <h1 class="text-xl font-bold mb-4">Daily Task Planner</h1>

    <div v-for="(task, index) in tasks" :key="index" class="border p-3 mb-2 rounded">
      <label>
        Task Name:
        <input v-model="task.task_name" type="text" class="border p-1 rounded w-full" />
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

    <div v-if="summary" class="mt-4 p-3 border rounded">
      <h2 class="font-bold">Summary:</h2>
      <p>Total hours: {{ summary.total_hours }}</p>
      <ul>
        <li v-for="task in summary.tasks" :key="task.task_name">
          {{ task.task_name }} - {{ task.duration_hours }} hours
        </li>
      </ul>
    </div>
  </div>
</template>

<style>
body {
  font-family: sans-serif;
}
</style>
