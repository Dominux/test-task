<template>
    <v-card>
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
        <v-data-table
          :headers="headers"
          :items="jobbers"
          :search="search"
          :sort-by="['name', 'companyName', 'positionName', 'hireDate', 'fireDate', 'salary', 'base', 'advance', 'byHours']"
          class="elevation-1"
        >
            
            <template v-slot:item="{ item }">
                <tr>
                    <td>{{ item.name }}</td>
                    <td>{{ item.companyName }}</td>
                    <td>{{ item.positionName }}</td>
                    <td>{{ item.hireDate }}</td>
                    <td>{{ item.fireDate }}</td>
                    <td>{{ item.salary }}руб ({{ item.fraction }} %)</td>
                    <td>{{ item.base }}</td>
                    <td>{{ item.advance }}</td>
                    <td>{{ item.byHours }}</td>
                </tr>
            </template>

        </v-data-table>
    </v-card>
</template>

<script>
    export default {
        data(){
            return {

                search: null,

                headers: [
                  {
                    text: 'Сотрудник',
                    align: 'left',
                    value: 'name',
                  },
                  { text: 'Название компании', value: 'companyName' },
                  { text: 'Позиция', value: 'positionName' },
                  { text: 'Дата найма', value: 'hireDate' },
                  { text: 'Дата увольнения', value: 'fireDate' },
                  { text: 'Зарплата', value: 'salary'},
                  { text: 'База', value: 'base' },
                  { text: 'Аванс', value: 'advance' },
                  { text: 'Почасовая', value: 'byHours' },
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
        } 
    }
</script>