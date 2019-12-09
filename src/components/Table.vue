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
                        <td @click="openDialog([
                            { column: 'Зарплата', name:  item.name },
                            { valueName: 'salary',  value: item.salary   },
                            { valueName: 'fraction', value: item.fraction }
                            ])"
                        >
                            {{ item.salary }}₽ ({{ item.fraction }}%)
                        </td>
                        <td @click="openDialog([
                            { column: 'База', name:  item.name },
                            { valueName: 'base',  value: item.base },
                            ])"
                        >
                            {{ item.base }}₽
                        </td>
                        <td @click="openDialog([
                            { column: 'Аванс', name:  item.name },
                            { valueName: 'advance',  value: item.advance },
                            ])"
                        >
                            {{ item.advance }}₽
                        </td>
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
                        v-bind:label="dialogVars[0].column"
                        v-model="dialogVars[1].value"
                        required
                    ></v-text-field>

                    <v-text-field
                        v-if="dialogVars[0].column == 'Зарплата'"
                        label="Процент"
                        v-model="dialogVars[2].value"
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
                dialogVars: [
                    {
                        column: null,
                        name: null,
                    },
                    {
                        valueName: null,
                        value: null,
                    },
                    {
                        valueName: null,
                        value: null,
                    },
                ],
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

            openDialog (arr) {
                for (var i = 0; i < arr.length; i++) {
                    if (i == 0){
                        this.dialogVars[i].column    = arr[i].column;
                        this.dialogVars[i].name      = arr[i].name;
                    } else {
                        this.dialogVars[i].valueName = arr[i].valueName;
                        this.dialogVars[i].value     = arr[i].value;
                    }
                }
                this.showDialog = true;
            },

            save () {

                for (var i = 0; i < this.jobbers.length; i++) {
                    if (this.jobbers[i].name == this.dialogVars[0].name) {
                        break;
                    }
                }

                for (var j = 0; j < Object.keys(this.jobbers[i]).length; j++) {
                    if (Object.keys(this.jobbers[i])[j] == this.dialogVars[1].valueName) {
                        this.jobbers[i][this.dialogVars[1].valueName] = this.dialogVars[1].value;
                    } else if (Object.keys(this.jobbers[i])[j] == this.dialogVars[2].valueName) {
                        this.jobbers[i][this.dialogVars[2].valueName] = this.dialogVars[2].value;
                    }
                }

                this.showDialog = false;

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