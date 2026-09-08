<template>
  <table class="custom-table">
    <tbody>
      <tr v-for="(group, groupIndex) in groupedData" :key="groupIndex">
        <template v-for="(item, itemIndex) in group" :key="itemIndex">
          <td>{{ tableHeaders[groupIndex * 2 + itemIndex] }}</td>
          <td>{{ item }}</td>
        </template>
        <!-- 补齐最后一行的空单元格 -->
        <template v-if="groupIndex === groupedData.length - 1 && group.length < 2">
          <td></td>
          <td></td>
        </template>
      </tr>
    </tbody>
  </table>
</template>

<script setup>
import { ref, computed } from 'vue';

// 表格表头数据，共 11 个表头
const tableHeaders = ref([
  '中文名', '拉丁学名', '界', '门', '纲',
  '目', '科', '属', '种', '命名者及年代',
  '濒危等级'
]);

// 表格主体数据，共 11 条数据
const tableData = ref([
  '问荆', ' Equisetumarvense L.', '  植物界', ' 蕨类植物门', '木贼纲',
  '木贼目', '木贼科', '木贼属', '问荆', 'L.1753',
  '无危（LC）'
]);

// 将数据每两个分为一组
const groupedData = computed(() => {
  const result = [];
  for (let i = 0; i < tableData.value.length; i += 2) {
    result.push(tableData.value.slice(i, i + 2));
  }
  return result;
});
</script>

<style scoped>
.custom-table {
  width: 95%;
  border-collapse: collapse;
  border: none;
  font-size: 10rpx;
}

.custom-table th, .custom-table td {
  padding: 10rpx;
  text-align: left;
  border-bottom: 2px dotted orange;
  border-top: none;
  border-left: none;
  border-right: none;
}
</style>