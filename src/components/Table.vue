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

                <template v-slot:item.data-table-select="props">
                    <div>
                        <v-checkbox
                            v-if="!props.item.fireDate"
                            color="green"
                            v-model="selected" 
                            :value="props.item" 
                            style="margin: 0px; padding: 0px" 
                            hide-details 
                        />
                    </div>
                </template>
                <template v-slot:item.name="props">
                    <div>{{ props.item.name }}</div>
                </template>
                <template v-slot:item.companyName="props">
                    <div>{{ props.item.companyName }}</div>
                </template>
                <template v-slot:item.positionName="props">
                    <div>{{ props.item.positionName }}</div>
                </template>
                <template v-slot:item.hireDate="props">
                    <div>{{ normalDate(props.item.hireDate) }}</div>
                </template>
                <template v-slot:item.fireDate="props">
                    <div>{{ normalDate(props.item.fireDate) }}</div>
                </template>
                <template v-slot:item.salary="props">
                    <div @click="openDialog([
                        { column: 'Зарплата', name: props.item.name, enable: !props.item.fireDate },
                        { valueName: 'salary',   value: props.item.salary   },
                        { valueName: 'fraction', value: props.item.fraction }
                        ])"
                    >
                        {{ props.item.salary }}₽ ({{ props.item.fraction }}%)
                    </div>
                </template>
                <template v-slot:item.base="props">
                    <div @click="openDialog([
                        { column: 'База', name: props.item.name, enable: !props.item.fireDate },
                        { valueName: 'base', value: props.item.base },
                        ])"
                    >
                        {{ props.item.base }}₽
                    </div>
                </template>
                <template v-slot:item.advance="props">
                    <div @click="openDialog([
                        { column: 'Аванс', name: props.item.name, enable: !props.item.fireDate },
                        { valueName: 'advance', value: props.item.advance },
                        ])"
                    >
                        {{ props.item.advance }}₽
                    </div>
                </template>
                <template v-slot:item.byHours="props">
                    <td>
                        <v-checkbox 
                            color="green"
                            v-model="props.item.byHours" 
                            style="margin: 0px; padding: 0px" 
                            hide-details
                            :disabled="isDisabledByHours(props.item)"
                        />
                    </td>
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
                rows: null,
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

        mounted () {
            this.setRedRows ();
        },

        updated () {
            this.setRedRows ();
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

            setRedRows () {
                const rows = document.getElementsByTagName('tr');
                for (var i = 1; i < rows.length; i++) {
                    if (rows[i].childElementCount !== 1) {
                        if (rows[i].children[5].children[0].innerHTML) {
                            rows[i].classList.add('fire-row')
                        }
                    }
                }
            },

        },

    }
</script>


<style>
    .fire-row {
        background-color: salmon;
    }
</style>