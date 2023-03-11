import { reactive } from 'vue';

export const ui = reactive({
    user: {
        access_token: undefined,
        info: {
            role: undefined,
        },
    },
    getDate(input) {
        let formatDate = new Date(input * 1000);
        let date = formatDate.getDate();
      
        let months = [
          'января',
          'февраля',
          'марта',
          'апреля',
          'мая',
          'июня',
          'июля',
          'августа',
          'сентября',
          'октября',
          'ноября',
          'декабря',
        ];
        let month = months[formatDate.getMonth()];
      
        return `${date} ${month}`;
    }
});