<template>

  <nav aria-label="Page Navigation" class="g-mb-50">
    <ul class="list-inline">
      <li class="list-inline-item">
        <router-link v-bind:to="{ path: $route.fullPath, query: { page: curPage - 1, per_page: perPage }}" v-bind:class="{'u-pagination-v1__item--disabled': curPage == 1}" class="u-pagination-v1__item u-pagination-v1-1 g-rounded-50 g-pa-12-21" aria-label="Previous">
          <span aria-hidden="true">
            <i class="fa fa-angle-left"></i>
          </span>
          <span class="sr-only">Previous</span>
        </router-link>
      </li>

      <li v-if="page != 'NaN'" v-for="(page, index) in iter_pages" v-bind:key="index" class="list-inline-item g-hidden-sm-down">
        <router-link v-bind:to="{ path: $route.fullPath, query: { page: page, per_page: perPage }}" v-bind:class="{'u-pagination-v1-1--active': $route.query.page == page || (!$route.query.page && page == 1)}" class="u-pagination-v1__item u-pagination-v1-1 g-rounded-50 g-pa-12-19">{{ page }}</router-link>
      </li>
      <li v-else class="list-inline-item g-hidden-sm-down">
        <span class="g-pa-12-19">...</span>
      </li>
      
      <li class="list-inline-item">
        <router-link v-bind:to="{ path: $route.fullPath, query: { page: curPage + 1, per_page: perPage }}" v-bind:class="{'u-pagination-v1__item--disabled': curPage == totalPages || totalPages == 0 }" class="u-pagination-v1__item u-pagination-v1-1 g-rounded-50 g-pa-12-21" aria-label="Next">
          <span aria-hidden="true">
            <i class="fa fa-angle-right"></i>
          </span>
          <span class="sr-only">Next</span>
        </router-link>
      </li>
      <li class="list-inline-item float-right">
        <span class="u-pagination-v1__item-info g-pa-12-19">Page {{ curPage }} of {{ totalPages }}</span>
      </li>
    </ul>
  </nav>

</template>

<script>
export default {
  name: 'Pagination',  // this is the name of the component
  props: {
    curPage: {
      required: true
    },
    perPage: {
      default: 3
    },
    totalPages: {
      required: true
    },
    leftPages: {
      default: 2
    },
    rightPages: {
      default: 2
    }
  },
  computed: {
    iter_pages: function () {
      // 构建分页导航，当前页左、右两边各显示2页，比如  1, 2, ... 7, 8, 9, 10, 11 ... 30, 31
      let arr = [1, 2]
      for (var i = this.leftPages; i > 0; i--) {
        arr.push(this.curPage - i)
      }
      arr.push(this.curPage)
      for (var i = 1; i <= this.rightPages; i++) {
        arr.push(this.curPage + i)
      }
      arr.push(this.totalPages - 1)
      arr.push(this.totalPages)
      
      
      // 小于1，或大于最大页数的都是非法的，要去除
      arr = arr.filter(item => item > 0 && item <= this.totalPages)
      // 去除重复项
      arr = [...new Set(arr)]
      // 假设当前页为1，总页数为6或6以上时，在倒数第2个位置插入特殊标记  1, 2, 3 ... 5, 6
      if (this.curPage + this.rightPages < this.totalPages - 2) {
        arr.splice(-2, 0, 'NaN')
      }
      // 当前页为6或6以上时，在第3个位置插入特殊标记  1, 2 ... 4, 5, 6
      if (this.curPage - this.leftPages - 1 > 2) {
        arr.splice(2, 0, 'NaN')
      }

      return arr
    }
  }
}
</script>