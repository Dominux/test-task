<template>
    <div>

        <v-card >
            <v-card-title>
                Занимаемые должности
                <v-spacer></v-spacer>
                <v-text-field
                    v-model="search"
                    append-icon="search"
                    label="Поиск по сотруднику"
                    single-line
                    hide-details
                ></v-text-field>
            </v-card-title>
            
            <v-container fluid>
                <v-layout justify-end>
                    <v-checkbox 
                        color="green" 
                        label="Показывать уволенных"
                        v-model="showFiredJobbers" 
                    />
                </v-layout>
            </v-container>  

            <v-data-table
                :headers="headers"
                :items="jobbers"
                :search="search"
                item-key="name"
                v-model="selected"
                show-select
                class="elevation-1"
            >
                
                <template v-slot:item="{ item }">
                    <tr 
                        v-bind:class="{'fire-row': item.fireDate}"
                        v-if="filterFiredJobbers(item)"
                    >
                        <td>
                            <v-checkbox
                                v-if="!item.fireDate"
                                color="green"
                                v-model="selected" 
                                :value="item" 
                                style="margin: 0px; padding: 0px" 
                                hide-details 
                            />
                        </td>
                        <td>{{ item.name }}</td>
                        <td>{{ item.companyName }}</td>
                        <td>{{ item.positionName }}</td>
                        <td>{{ item.hireDate }}</td>
                        <td>{{ item.fireDate }}</td>
                        <td @click="openDialog('Зарплата', item.salary, item.name)">{{ item.salary }}₽ ({{ item.fraction }}%)</td>
                        <td>{{ item.base }}₽</td>
                        <td>{{ item.advance }}₽</td>
                        <td>
                            <v-checkbox 
                                color="green"
                                v-model="item.byHours" 
                                style="margin: 0px; padding: 0px" 
                                hide-details 
                            />
                        </td>
                    </tr>
                </template>

            </v-data-table>
        </v-card>

        <v-container 
            fluid
            v-if="showDialog"
        >
            <v-card>
                <template>
                  <v-form
                    ref="form"
                    lazy-validation
                  >
                    <v-text-field
                      v-bind:label="dialogVars.title"
                      v-model="dialogVars.value"
                      required
                    ></v-text-field>

                    <v-btn
                      color="success"
                      class="mr-4"
                      @click="cancel()"
                      text
                    >
                      Отменить
                    </v-btn>

                    <v-btn
                      color="success"
                      class="mr-4"
                      @click="save()"
                      text
                    >
                      Сохранить
                    </v-btn>

                  </v-form>
                </template>
            </v-card>
        </v-container>  
    
    </div>

</template>



<script>
    export default {

        data(){
            return {
                showFiredJobbers: true,
                showDialog: false,
                dialogVars: {
                    title: null,
                    value: null,
                    name: null,
                },
                search: null,
                selected: [],
                headers: [
                    {
                        text: 'Сотрудник',
                        align: 'left',
                        value: 'name',
                    },
                    { text: 'Название компании', value: 'companyName',  filterable: false },
                    { text: 'Позиция',           value: 'positionName', filterable: false },
                    { text: 'Дата найма',        value: 'hireDate',     filterable: false },
                    { text: 'Дата увольнения',   value: 'fireDate',     filterable: false },
                    { text: 'Ставка',            value: 'salary',       filterable: false },
                    { text: 'База',              value: 'base',         filterable: false },
                    { text: 'Аванс',             value: 'advance',      filterable: false },
                    { text: 'Почасовая',         value: 'byHours',      filterable: false },
                ],
                jobbers: [
                    {
                        name: 'Джордж Вашингтон',
                        companyName: 'ООО "Синергия"',
                        positionName: 'Первый президент США',
                        hireDate: '1789-04-30',
                        fireDate: '1797-03-04',
                        salary: 1000,
                        fraction: 100,
                        base: 1000,
                        advance: 1000,
                        byHours: false
                    },
                    {
                        name: 'Ричард I Львиное Сердце',
                        companyName: 'ООО "Синергия"',
                        positionName: 'Король Англии',
                        hireDate: '1189-01-01',
                        fireDate: '1199-05-17',
                        salary: 1000,
                        fraction: 100,
                        base: 1000,
                        advance: 1000,
                        byHours: true
                    },
                    {
                        name: 'Джейсон Стейтем',
                        companyName: 'ООО "Синергия"',
                        positionName: 'Бейкон',
                        hireDate: '1998-09-01',
                        fireDate: null,
                        salary: 1000,
                        fraction: 100,
                        base: 1000,
                        advance: 1000,
                        byHours: false
                    },
                    {
                        name: 'Тарантино К. Дж.',
                        companyName: 'ООО "Синергия"',
                        positionName: 'Джимми',
                        hireDate: '1994-04-15',
                        fireDate: null,
                        salary: 1000,
                        fraction: 100,
                        base: 1000,
                        advance: 1000,
                        byHours: false
                    },
                    {
                        name: 'Камбербэтч Б.',
                        companyName: 'ООО "Синергия"',
                        positionName: 'Смауг',
                        hireDate: '1000-01-01',
                        fireDate: '2941-10-09',
                        salary: 1000,
                        fraction: 100,
                        base: 1000,
                        advance: 1000,
                        byHours: false
                    },
                    {
                        name: 'Крузенштерн И. Ф.',
                        companyName: 'ООО "Синергия"',
                        positionName: 'Человек и пароход',
                        hireDate: '1770-11-08',
                        fireDate: null,
                        salary: 1000,
                        fraction: 100,
                        base: 1000,
                        advance: 1000,
                        byHours: false
                    },
                    {
                        name: 'Бендер С. Р.',
                        companyName: '"Planet Express"',
                        positionName: 'Робот-сгибальщик',
                        hireDate: '2997-03-27',
                        fireDate: null,
                        salary: 1000,
                        fraction: 100,
                        base: 1000,
                        advance: 1000,
                        byHours: true
                    }
                ]
            }
        },

        methods: {
            filterFiredJobbers (item) {
                return !item.fireDate || this.showFiredJobbers
            },

            openDialog (title, value, name) {
                this.showDialog       = true;

                this.dialogVars.title = title;
                this.dialogVars.value = value;
                this.dialogVars.name  = name;
            },

            save () {
                for (var i = 0; i < this.jobbers.length; i++) {
                    if (this.jobbers[i].name == this.dialogVars.name) {
                        this.jobbers[i].salary = this.dialogVars.value;
                        this.showDialog = false;
                        break;
                    }
                }
            },

            cancel () {
                this.showDialog = false;
            },

        },

    }
</script>



<style>
    .fire-row {
        background-color: salmon;
    }
</style>