<template>
  <div>
    <h3>Here is your to do list for:</h3>
    <h4><font-awesome-icon icon="arrow-circle-left" fixed-width @click="previousDay();" class="point_cursor"/> {{ this.formatDate(current_date) }} <font-awesome-icon icon="arrow-circle-right" fixed-width @click="nextDay();" class="point_cursor"/></h4>
    <div id="task-list">
      <ToDoItem v-for="item in todo_list" :key="item.id" :item="item"/>
    </div>
    <h4 v-if="todo_list.length == 0 && !in_creation">Nothing on your to do list!</h4>
    <div v-if="in_creation" id="create-form">
      <form v-on:submit.prevent="saveNewItem">
        <div class="form-row">
          <div class="col-2">
            <input type="text" class="form-control" v-model="new_item.title" placeholder="Title" />
          </div>
          <div class="col">
            <textarea class="form-control" rows="1" v-model="new_item.description" placeholder="Description" />
          </div>
          <div class="col-1">
            <button type="submit" class="btn btn-block btn-success">Save</button>
          </div>
        </div>
      </form>
    </div>
    <div v-if="todo_list.length < 6 && !in_creation">
      <button class="btn btn-primary" style="margin-top: 10px;" @click="createToDo()">Add To Do</button>
    </div>
  </div>
</template>

<script>
import ToDoItem from '../components/ToDoItem'
import Sortable from "sortablejs";

export default {
  name: "ToDoView",
  components: {
    ToDoItem
  },
  data: function () {
    return {
      todo_list: [],
      current_date: null,
      in_creation: false,
      new_item: {
        title: '',
        description: ''
      }
    }
  },
  computed: {
  },
  methods: {
    getToDoList: function(date) {
      return this.axios.get("/todo_item/?date=" + this.formatDate(date),
      {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.access_token
        }
      }).then(response => {
        this.todo_list = response.data.results.sort((a, b) => {
          return a.priority - b.priority;
        });
      }).catch(err => {
        if (err.response.status >= 400 & err.response.status <= 401) {
          this.$router.push("/login");
        }
      });
    },
    nextDay: function() {
      this.todo_list = [];
      this.in_creation = false;
      let d = new Date(this.current_date);
      d.setDate(d.getDate() + 1);
      this.current_date = d;
      this.getToDoList(this.current_date);
    },
    previousDay: function() {
      this.todo_list = [];
      this.in_creation = false;
      let d = new Date(this.current_date);
      d.setDate(d.getDate() - 1);
      this.current_date = d;
      this.getToDoList(this.current_date);
    },
    createToDo: function() {
      this.in_creation = true;
    },
    saveNewItem: function() {
      return this.axios.post("/todo_item/",
      {
        title: this.new_item.title,
        description: this.new_item.description,
        date: this.formatDate(this.current_date)
      },
      {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.access_token
        }
      }).then(response => {
        this.in_creation = false;
        this.todo_list.push(response.data);
        this.new_item = { 
          title: '',
          description: ''
         }

      }).catch(err => {
        if (err.response.status >= 400 & err.response.status <= 401) {
          this.$router.push("/login");
        }
      });
    },
    updateItem: function(item) {
      return this.axios.put("/todo_item/" + item.id + "/",
      {
        title: item.title,
        description: item.description,
        date: item.date,
        priority: item.priority
      },
      {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.access_token
        }
      }).catch(err => {
        if (err.response.status >= 400 & err.response.status <= 401) {
          this.$router.push("/login");
        }
      });
    }

  },
  mounted: function () {
    this.current_date = new Date();
    this.getToDoList(this.current_date);
    var sortableList = document.getElementById("task-list");
    Sortable.create(sortableList, {
      handle: '.drag-handle',
      animation: 150,
      onEnd: evnt => {
        for (let i = 0; i < evnt.to.childNodes.length; i++) {
          let id = evnt.to.childNodes[i].attributes["data-itemid"].nodeValue;
          let task = this.todo_list.find(el => {
            return el.id == id;
          });
          if (task.priority != i + 1) {
            // Only send an update if the priority has actually changed.
            task.priority = i + 1;
            this.updateItem(task);
          }
        }
      }
    });
  }
}
</script>

<style scoped>
  .point_cursor {
    cursor: pointer;
  }

  #create-form {
    margin-top: 15px;
  }
</style>

