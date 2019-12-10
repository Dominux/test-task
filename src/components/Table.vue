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
                <v-layout justify-end align-center>
                    <v-checkbox 
                        color="green" 
                        label="Показывать уволенных"
                        v-model="showFiredJobbers" 
                    />
                    <v-btn 
                        class="mr-2 ml-2" 
                        color="green accent-2"
                    >
                        Принять на должность
                    </v-btn>
                    <v-btn
                        class="mr-2 ml-2"
                        color="red accent-1"
                        :disabled="isSelectedEmpty"
                    >
                        {{ fireLabel }}
                    </v-btn>
                </v-layout>
            </v-container>  

            <v-data-table
                :headers="headers"
                :items="currentJobbers"
                :search="search"
                item-key="name"
                v-model="selected"
                show-select
                class="elevation-1"
            >
                
                <template v-slot:item="{ item }">
                    <tr v-bind:class="{'fire-row': item.fireDate}">
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
                        <td>{{ normalDate(item.hireDate) }}</td>
                        <td>{{ normalDate(item.fireDate) }}</td>
                        <td @click="openDialog([
                            { column: 'Зарплата', name: item.name, enable: !item.fireDate },
                            { valueName: 'salary',   value: item.salary   },
                            { valueName: 'fraction', value: item.fraction }
                            ])"
                        >
                            {{ item.salary }}₽ ({{ item.fraction }}%)
                        </td>
                        <td @click="openDialog([
                            { column: 'База', name: item.name, enable: !item.fireDate },
                            { valueName: 'base', value: item.base },
                            ])"
                        >
                            {{ item.base }}₽
                        </td>
                        <td @click="openDialog([
                            { column: 'Аванс', name: item.name, enable: !item.fireDate },
                            { valueName: 'advance', value: item.advance },
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
                                :disabled="isDisabledByHours(item)"
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
            <v-card 
                class="ma-10"
                max-width="400"
                raised
            >
                <v-card-text class="justify-center">
                        <v-col>
                            <v-row justify="center">
                                <v-col cols="12" md="6">
                                    <v-text-field
                                        v-bind:label="dialogVars[0].column"
                                        v-model="dialogVars[1].value"
                                    ></v-text-field>
                                </v-col>
                                <v-col md="6">
                                    <v-text-field
                                        v-if="dialogVars[0].column == 'Зарплата'"
                                        label="Процент"
                                        v-model="dialogVars[2].value"
                                    ></v-text-field>
                                </v-col>
                            </v-row>
                            <v-row justify="center">    
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
                            </v-row>
                        </v-col>    
                </v-card-text>

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

        computed: {

            fireLabel () {
                if (this.selected.length <= 1) { 
                    return "Снять с должности"
                } else {
                    return "Снять с должностей"
                }
            },

            isSelectedEmpty () {
                return this.selected.length === 0
            },

            currentJobbers () {
                if (this.showFiredJobbers) {
                    return this.jobbers
                } else {
                    const realJobbers = [];
                    for (var i = 0; i < this.jobbers.length; i++) {
                        if (!this.jobbers[i].fireDate) {
                            realJobbers.push(this.jobbers[i])
                        }
                    }
                    return realJobbers
                }
            },

        },

        methods: {

            normalDate (date) {
                if (date !== null) {
                    return date.split('-').reverse().join('.')
                } else {
                    return null  
                }
            },

            filterFiredJobbers (item) {
                return !item.fireDate || this.showFiredJobbers
            },

            isDisabledByHours (item) {
                if (item.fireDate) {
                    return true
                } else {
                    return false
                }
            },

            openDialog (arr) {

                if (arr[0].enable) {
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
                } else {
                    this.showDialog = false;
                }

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