import { loadResource } from "../../static/utils/resources.js";

export default {
  template: "<div></div>",
  props: {
    options: Object, // 确保 options 是 Object
    resource_path: String,
  },
  async mounted() {
    await this.$nextTick(); // NOTE: wait for window.path_prefix to be set
    await loadResource(window.path_prefix + `${this.resource_path}/index.global.min.js`);
    this.options.eventClick = (info) => this.$emit("click", { info });
    this.options.eventDrop = (info) => this.$emit("eventDrop", { info });
    this.options.eventResize = (info) => this.$emit("eventResize", { info });
    this.options.dateClick = (info) => {
      if (this.lastClick && (new Date() - this.lastClick < 300)) {
        this.$emit("dateDblClick", { info });
      } else {
        this.lastClick = new Date();
      }
    };
    this.calendar = new FullCalendar.Calendar(this.$el, this.options);
    this.calendar.render();
  },
  methods: {
    update_calendar() {
      if (this.calendar) {
        this.calendar.setOption("events", this.options.events);
        this.calendar.render();
      }
    },
  },
};
