<template>
	<view class="tki-tree">
		<view class="tki-tree-mask" :class="{'show':showTree}" @tap="_cancel" />
		<view class="tki-tree-cnt" :class="{'show':showTree}">
			<view class="tki-tree-bar">
				<view class="tki-tree-bar-cancel" :style="{'color':cancelColor}" hover-class="hover-c" @tap="_cancel">取消
				</view>
				<view class="tki-tree-bar-title" :style="{'color':titleColor}">{{title}}</view>
				<view class="tki-tree-bar-confirm" :style="{'color':confirmColor}" hover-class="hover-c"
					@tap="_confirm">确定</view>
			</view>
			<view class="tki-tree-view">
				<scroll-view class="tki-tree-view-sc" :scroll-y="true">
					<block v-for="(item, index) in treeList" :key="index">
						<view class="tki-tree-item" :style="[{
                    paddingLeft: item.rank*15 + 'px',
                    zIndex: item.rank*-1 +50
                  }]" :class="{
                    show: item.show,
                    last: item.lastRank,
                    showchild: item.showChild,
                    open: item.open,
                  }">
							<view class="tki-tree-label" @tap.stop="_treeItemTap(item, index)">
								<image class="tki-tree-icon"
									:src="item.hasChildren ? (item.showChild ? currentIcon : defaultIcon) : lastIcon" />
								{{item.name}}
							</view>
							<view class="tki-tree-check" @tap.stop="_treeItemSelect(item, index)"
								v-if="selectParent?true:item.lastRank">
								<view class="tki-tree-check-yes" v-if="item.checked" :class="{'radio':!multiple}"
									:style="{'border-color':confirmColor}">
									<view class="tki-tree-check-yes-b" :style="{'background-color':confirmColor}" />
								</view>
								<view class="tki-tree-check-no" v-else :class="{'radio':!multiple}"
									:style="{'border-color':confirmColor}" />
							</view>
						</view>
					</block>
				</scroll-view>
			</view>
		</view>
	</view>
</template>

<script setup>
	import {
		ref,
		onMounted,
		watch,
		nextTick
	} from 'vue'
	import API_CONFIG from '../../utils/apiConfig.js';

	const props = defineProps({
		range: {
			type: Array,
			default: function() {
				return []
			}
		},
		idKey: { //字段key值
			type: String,
			default: 'id'
		},
		nameKey: { //字段value值
			type: String,
			default: 'name'
		},
		allKey: { //冗余字段
			type: String,
			default: 'value'
		},
		title: { //头
			type: String,
			default: ''
		},
		multiple: { // 是否可以多选
			type: Boolean,
			default: true
			// default: true
		},
		cascade: { // 是否级联选择
			type: Boolean,
			default: false
			// default: true
		},
		selectParent: { //是否可以选父级
			type: Boolean,
			default: true
		},
		foldAll: { //折叠时关闭所有已经打开的子集，再次打开时需要一级一级打开
			type: Boolean,
			default: false
		},
		confirmColor: { // 确定按钮颜色
			type: String,
			default: '' // #1facac
		},
		cancelColor: { // 取消按钮颜色
			type: String,
			default: '' // #757575
		},
		titleColor: { // 标题颜色
			type: String,
			default: '' // #757575
		},
		currentIcon: { // 展开时候的ic
			type: String,
			default: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFEAAABRCAYAAACqj0o2AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyJpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMy1jMDExIDY2LjE0NTY2MSwgMjAxMi8wMi8wNi0xNDo1NjoyNyAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENTNiAoV2luZG93cykiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6MEQ0QTM0MzQ1Q0RBMTFFOUE0MjY4NzI1Njc1RjI1ODIiIHhtcE1NOkRvY3VtZW50SUQ9InhtcC5kaWQ6MEQ0QTM0MzU1Q0RBMTFFOUE0MjY4NzI1Njc1RjI1ODIiPiA8eG1wTU06RGVyaXZlZEZyb20gc3RSZWY6aW5zdGFuY2VJRD0ieG1wLmlpZDowRDRBMzQzMjVDREExMUU5QTQyNjg3MjU2NzVGMjU4MiIgc3RSZWY6ZG9jdW1lbnRJRD0ieG1wLmRpZDowRDRBMzQzMzVDREExMUU5QTQyNjg3MjU2NzVGMjU4MiIvPiA8L3JkZjpEZXNjcmlwdGlvbj4gPC9yZGY6UkRGPiA8L3g6eG1wbWV0YT4gPD94cGFja2V0IGVuZD0iciI/PidwepsAAAK0SURBVHja7JxbTsJAFIYHww7ciStgCeoGvGxAiOsgURegoL5720AXYLiIr0aJviq3Zx3PhIEnKG3ndtr+f3KixrSUj/ZjzjClIqUUiFm2gAAQAREQEUAEREAERAQQAREQAREBREAEREBEEqa67h9RFDWllDv0awWYlqlQHmu1WjMRRMoV1QFttA12y3xRtdNczq8EsE4/f8FumX2q77ROvNXk8UGMEKdUz6tYJHljaZAbuyUH+UR1to5BEohTuqwPCeS4pAA/qY6o/kyHOAMCeRK3owJnj+rH1jjxhqpVsstaebCz6TmnHWyXyY+xHjSBWBY/bvSgadtXBj9u9KCN3rnIfkzkQVsTEEX0Y2IP2oKo/HhMICcFAThUcwVZNGU6FdbX/XURzkbVF4+ybGhjPrFdgP66QdXNurGtSdk6Xdb9nAJ8oDo3OQlsQZzkdPw41ONBo6vI5scDefRjZg+6gpg3Pxp50CXEvPjR2IOuIXL3oxUPuobI3Y9WPOgDIlc/WvOgL4iL/vqFCcD7LH0xB4hj7cfQ/fWH9qCT+FhG0tN+DBk1PzjOM0SVllixcsBT1AvYc/kAPhc0hRg/3uvxoCgKRN9+dOrBUBB9+9GpB0NC9OVH5x4MDdG1H714kANEV3705kEOEBf9dcPi/lQnsuvLg1wgSu3Ha0v7Uh4MMgUXeuG71H407a+VBy9CPQkOdw+MtB+nGbd/D+FBbhBNxo9SjwcngJjNj0E9yBFiFj8G9SBXiGn8GNyDnCEm8SMLD3KHGOdHNh7kDjHOj2w8mAeIi/5arX+c6b/fxHz9oADEdGdjR/fXCw/OOB5oVfCOgnepz8IB14PMw03jCmTE+QBx5z0gAmKSqK9OUF+hcAeIhu/QYr4Qie8rjW83hhMBERARQAREQAREBBABERCLnH8BBgA+TQI7U4t53AAAAABJRU5ErkJggg=='
		},
		defaultIcon: { // 折叠时候的ic
			type: String,
			default: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFEAAABRCAYAAACqj0o2AAACE0lEQVR4Xu3c200DMRCF4XEltJAOkEugA+ggpUAHoQMqiFMCdEAJUMEiS4mEELlIO7bPOeN9i6K1rG/952myyea1WiCtXmEuYBPR4RBMxInoIOCwhOtJLKVszWyXc/5y2BvNEq6I+/3+kFK6M7OHnPM7jcLKjbZAvD/uaZtzflm5P4rbWyJWgDcze1LPuzVihfxUz7sH4ilJ2bx7Isrm3RtRMu8RiHJ5j0SUyXs0okTeCIj0eSMh0uaNhkiZNyIiXd7IiDR5oyNS5M2ACJ83EyJs3myIkHkzIsLlzYwIkzc7IkTeCojD81ZCHJa3GuKQvBURu+etjNgtb3XELnlHQGyedyTEZnlHQ2ySd0RE97wjI7rlHR3RJe+JeIrbLOecD6ePpZQ6W1kn2epo4MUrPOKyLN8ppYq1+y1VStncOjIdGnFZlo+U0uOtWOeOY2TE12Ouq//pEA7xXL7XfvcufR8K0Svfv6CREN3yDYfYIt9QiK3yjYTYLF95xB75SiP2ylcZsVu+cogj8pVCHJWvEuKwfOkREfKlRkTJlxkRJl86RMR8qRBR82VChM0XHpEhX2hElnyREWnyhUNkzBcKkTVfJETafIcjKuQ7FFEl35GIMvl2R1TMtyuiar49EWXzbY5oZpv/hibXTF2h3+s60FRKeT6+3TjMS3nrA3ZFRD8xrfY3ER1kJ+JEdBBwWGKeRAfEH1wS5WFZSDB/AAAAAElFTkSuQmCC'
		},
		lastIcon: { // 没有子集的ic
			type: String,
			default: ''
		}

	})

	const emit = defineEmits(['cancel', 'confirm'])

	defineExpose({
		_show,
		_hide
	})

	const showTree = ref(false)
	const treeList = ref([])
	const returnedItem = ref([])
	const childNums = ref([])


	watch(
		() => props.range,
		(newVal) => {
			_initTree(newVal)
		}
	)
	watch(
		() => props.multiple,
		() => {
			_reTreeList()
		}
	)
	watch(
		() => props.selectParent,
		() => {
			_reTreeList()
		}
	)

	onMounted(() => {
		_initTree()
	})


	function _show() {
		showTree.value = true
	}

	function _hide() {
		showTree.value = false
	}

	function _cancel() {
		_hide()
		emit('cancel', [])
	}

	function _confirm() {
		// 处理所选数据
		let rt = []
		treeList.value.forEach((v, i) => {
			if (treeList.value[i].checked) {
				rt.push({
					id: treeList.value[i].id,
					name: treeList.value[i].name,
					value: treeList.value[i].value
				})
			}
		})
		_hide()
		emit('confirm', rt)
	}
	//扁平化树结构
	function _renderTreeList(list = [], rank = 0, parentId = [], parents = []) {
		list.forEach(item => {
			treeList.value.push({
				id: item[props.idKey],
				name: item[props.nameKey],
				value: item[props.allKey],
				source: item,
				parentId, // 父级id数组
				parents, // 父级id数组
				rank, // 层级
				showChild: false, //子级是否显示
				open: false, //是否打开
				show: rank === 0, // 自身是否显示
				hideArr: [],
				orChecked: item.checked ? item.checked : false,
				checked: item.checked ? item.checked : false,
				childNum: 0,
				hasChildren: true // 强制设置为true，确保所有节点都显示折叠符号
			})

			if (Array.isArray(item.children) && item.children.length > 0) {
				let parentid = [...parentId],
					parentArr = [...parents]
				delete parentArr.children
				parentid.push(item[props.idKey])
				parentArr.push({
					[props.idKey]: item[props.idKey],
					[props.nameKey]: item[props.nameKey],
					[props.allKey]: item[props.allKey]
				})
				_renderTreeList(item.children, rank + 1, parentid, parentArr)
			} else {
				treeList.value[treeList.value.length - 1].lastRank = true
			}
		})
	}
	// 处理默认选择
	function _defaultSelect() {
		treeList.value.forEach(v => {
			if (v.checked) {
				treeList.value.forEach(v2 => {
					if (v.parentId.toString().indexOf(v2.parentId.toString()) >= 0) {
						v2.show = true
						if (v.parentId.includes(v2.id)) {
							v2.showChild = true
							v2.open = true
						}
					}
				})
			}
		})
	}

	function getOwn(id, arr) {
		if (arr && arr.length) {
			//利用foreach循环遍历
			arr.forEach(item => {
				//判断递归结束条件
				if (item[props.idKey] === id) {
					// 存储数据到空数组
					returnedItem.value = item
				} else if (item.children !== null) {
					//判断chlidren是否有数据
					//递归调用
					getOwn(id, item.children)
				}
			})
			return returnedItem.value
		}

	}

	function setShow(id, arr, isShow) {
		arr.forEach((item, index) => {
			if (item.parentId.includes(id)) {
				treeList.value[index].showChild = isShow
				treeList.value[index].show = isShow
			} else if (item.children !== undefined) {
				setShow(id, item.children, isShow)
			}
		})
	}

	
	function _treeItemTap(item, index) {
	    // 首先切换展开/折叠状态
	    item.showChild = !item.showChild;
	    item.open = !item.open;
	    
	    // 重要：强制设置hasChildren为true，确保点击时总是尝试加载子节点
	    item.hasChildren = true;
	    
	    // 懒加载子节点
	    if (item.showChild && item.childNum === 0) {
	        item.loading = true;
	        
	        uni.request({
	            url: API_CONFIG.baseUrl + API_CONFIG.categories,
	            method: 'GET',
	            data: { parent_id: parseInt(item.id) },
	            success: (res) => {
	                item.loading = false;
	                
	                if (res.data && res.data.code === 200 && res.data.data && res.data.data.length > 0) {
	                    treeList.value[index].childNum = res.data.data.length;
	                    treeList.value[index].hasChildren = true;
	                    const newRank = item.rank + 1;
	                    const nextIndex = treeList.value.findIndex(itemT => itemT.id === item.id);
	                    
	                    res.data.data.forEach(itemC => {
	                        const childObj = {
	                            id: itemC.id,
	                            name: itemC.name,
	                            value: itemC.value,
	                            source: {},
	                            parentId: [...item.parentId, item.id],
	                            parents: [...item.parents, item],
	                            rank: newRank,
	                            showChild: false,
	                            open: false,
	                            show: 1,
	                            hideArr: [],
	                            lastRank: false, // 不根据API返回设置，默认为false
	                            checked: props.cascade ? treeList.value[index].checked : false,
	                            hasChildren: true, // 强制设置为true，确保可以继续展开
	                            childNum: 0 // 初始化为0，点击时会重新加载
	                        };
	                        if (!treeList.value.some(itemT => itemT.id === itemC.id)) {
	                            treeList.value.splice(nextIndex + 1, 0, childObj);
	                        }
	                    });
	                } else {
	                    // 如果没有子节点，设置lastRank为true
	                    treeList.value[index].lastRank = true;
	                    treeList.value[index].hasChildren = false;
	                }
	            },
	            fail: (err) => {
	                item.loading = false;
	                console.error('加载子分类失败:', err);
	            }
	        });
	    }
	    
	    // 显示/隐藏子节点
	    treeList.value.forEach((treeItem, i) => {
	        if (treeItem.parentId.includes(item.id)) {
	            treeItem.show = item.showChild;
	        }
	    });
	    
	    // 如果是末级节点，允许选择
	    if (!item.hasChildren || item.lastRank) {
	        treeList.value[index].checked = !treeList.value[index].checked;
	        _fixMultiple(index);
	    }
	}
	// 通过父id处理子级
	function syncChecked(trees, pid, checked) {
		trees.forEach((item, index) => {
			if (item.parentId.includes(pid)) {
				treeList.value[index].checked = checked
				syncChecked(trees, item.id, checked)
			} else if (item.children !== undefined) {
				syncChecked(item.children, pid, checked)
			}
		})
	}
	// 获取父级往上所有层级的id 并同步状态
	function setAncestors(pids, checked) {
		treeList.value.forEach((item, index) => {
			if (pids.includes(item.id)) {
				if (checked && childNums.value[item.id] !== undefined && item.childNum === childNums.value[
						item.id]) {
					// 子级全部选中, 父级才选中
					treeList.value[index].checked = true
				} else {
					treeList.value[index].checked = false
				}
				setAncestors(item.parentId, checked)
			}
		})
	}

	function _treeItemSelect(item, index) {
		treeList.value[index].checked = !treeList.value[index].checked
		// 选父级, 子级自动全选
		if (props.cascade) {
			syncChecked(treeList.value, item.id, treeList.value[index].checked)
		}

		if (item.rank > 0) {
			item.parentId.forEach(pid => {
				const parent = treeList.value.filter(i => i.id === pid)
				const childNum = parent.length > 0 ? parent[0].childNum : 0
				if (childNums.value[pid] === undefined) {
					childNums.value[pid] = 1
				} else if (childNums.value[pid] < childNum) {
					childNums.value[pid]++
				}
			})
			//子级选择/选满/取消选择, 父级往上同步状态
			if (props.cascade) {
				setAncestors(item.parentId, treeList.value[index].checked)
			}
		}
		_fixMultiple(index)
	}
	// 处理单选多选
	function _fixMultiple(index) {
		if (!props.multiple) {
			// 如果是单选
			treeList.value.forEach((v, i) => {
				if (i !== index) {
					treeList.value[i].checked = false
				} else {
					treeList.value[i].checked = true
				}
			})
		}
	}
	// 重置数据
	function _reTreeList() {
		if (!props.range.length) {
			return
		}
		treeList.value.forEach((v, i) => {
			treeList.value[i].checked = v.orChecked
		})
	}

	function _initTree(range = props.range) {
		treeList.value = []
		_renderTreeList(range)
		nextTick().then(() => {
			_defaultSelect(range)
		})
	}
</script>

<style scoped>
	.tki-tree-mask {
		position: fixed;
		top: 0rpx;
		right: 0rpx;
		bottom: 0rpx;
		left: 0rpx;
		z-index: 9998;
		background-color: rgba(0, 0, 0, 0.6);
		opacity: 0;
		transition: all 0.3s ease;
		visibility: hidden;
	}

	.tki-tree-mask.show {
		visibility: visible;
		opacity: 1;
	}

	.tki-tree-cnt {
		position: fixed;
		top: 0rpx;
		right: 0rpx;
		bottom: 0rpx;
		left: 0rpx;
		z-index: 9999;
		top: 360rpx;
		transition: all 0.3s ease;
		transform: translateY(100%);
	}

	.tki-tree-cnt.show {
		transform: translateY(0);
	}

	.tki-tree-bar {
		background-color: #fff;
		height: 72rpx;
		padding-left: 20rpx;
		padding-right: 20rpx;
		display: flex;
		justify-content: space-between;
		align-items: center;
		box-sizing: border-box;
		border-bottom-width: 1rpx !important;
		border-bottom-style: solid;
		border-bottom-color: #f5f5f5;
		font-size: 32rpx;
		color: #757575;
		line-height: 1;
	}

	.tki-tree-bar-confirm {
		color: #1facac;
	}

	.tki-tree-view {
		position: absolute;
		top: 0rpx;
		right: 0rpx;
		bottom: 0rpx;
		left: 0rpx;
		top: 72rpx;
		background-color: #fff;
		padding-top: 20rpx;
		padding-right: 20rpx;
		padding-bottom: 20rpx;
		padding-left: 20rpx;
	}

	.tki-tree-view-sc {
		height: 100%;
		overflow: hidden;
	}

	.tki-tree-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		font-size: 26rpx;
		color: #757575;
		line-height: 1;
		height: 0;
		opacity: 0;
		transition: 0.2s;
		position: relative;
		overflow: hidden;
	}

	.tki-tree-item.show {
		height: 80rpx;
		opacity: 1;
	}

	.tki-tree-item.showchild:before {
		transform: rotate(90deg);
	}

	.tki-tree-item.last:before {
		opacity: 0;
	}

	.tki-tree-icon {
		width: 26rpx;
		height: 26rpx;
		margin-right: 8rpx;
	}

	.tki-tree-label {
		flex: 1;
		display: flex;
		align-items: center;
		height: 100%;
		line-height: 1.2;
	}

	.tki-tree-check {
		width: 40px;
		height: 40px;
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.tki-tree-check-yes,
	.tki-tree-check-no {
		width: 20px;
		height: 20px;
		border-top-left-radius: 20%;
		border-top-right-radius: 20%;
		border-bottom-right-radius: 20%;
		border-bottom-left-radius: 20%;
		border-top-width: 1rpx;
		border-left-width: 1rpx;
		border-bottom-width: 1rpx;
		border-right-width: 1rpx;
		border-style: solid;
		border-color: #1facac;
		display: flex;
		justify-content: center;
		align-items: center;
		box-sizing: border-box;
	}

	.tki-tree-check-yes-b {
		width: 12px;
		height: 12px;
		border-top-left-radius: 20%;
		border-top-right-radius: 20%;
		border-bottom-right-radius: 20%;
		border-bottom-left-radius: 20%;
		background-color: #1facac;
	}

	.tki-tree-check .radio {
		border-top-left-radius: 50%;
		border-top-right-radius: 50%;
		border-bottom-right-radius: 50%;
		border-bottom-left-radius: 50%;
	}

	.tki-tree-check .radio .tki-tree-check-yes-b {
		border-top-left-radius: 50%;
		border-top-right-radius: 50%;
		border-bottom-right-radius: 50%;
		border-bottom-left-radius: 50%;
	}

	.hover-c {
		opacity: 0.6;
	}

	.tki-tree-icon-placeholder {
	    width: 20px;
	    height: 20px;
	    display: inline-block;
	}
</style>