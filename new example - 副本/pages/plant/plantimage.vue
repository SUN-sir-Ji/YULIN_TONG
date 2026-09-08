<template>
    <view  class="content">
        <view class="up" >
			<view style="display: flex; flex-direction: column; width: 100%;margin-top:9% ;"@click="$emit('goToPlantHome')">
			  <uni-icons type="left" size="30" style="align-self: flex-start;" ></uni-icons>
			</view>
				<text class="title">问荆[wèn jīng]</text>
                <text class="class">木贼科木贼属植物</text>		
        </view>
     
        <view class="down">
                <view class="picture">
                    <image src="/static/plantphoto/plant.png" style="width:35%;height:100%;flex-shrink: 0;margin-right: 1%;border-radius: 15rpx;" />
                    <image src="/static/plantphoto/plant.png" style="width:35%;height:100%;flex-shrink: 0;margin-right: 1%;border-radius: 15rpx;" />
                    <image src="/static/plantphoto/plant.png" style="width:35%;height:100%;flex-shrink: 0;margin-right: 1%;border-radius: 15rpx;" />
                    <image src="/static/plantphoto/plant.png" style="width:35%;height:100%;flex-shrink: 0;margin-right: 1%;border-radius: 15rpx;" />
                    <image src="/static/plantphoto/plant.png" style="width:35%;height:100%;flex-shrink: 0;margin-right: 1%;border-radius: 15rpx;" />
                    <image src="/static/plantphoto/plant.png" style="width:35%;height:100%;flex-shrink: 0;margin-right: 1%;border-radius: 15rpx;" />
                </view>
               <TableComponent />
        </view>
    </view>   

</template>
<script>
import TableComponent from '/components/InformationTable/table.vue';
import uniIcons from '@/uni_modules/uni-icons/components/uni-icons/uni-icons.vue';
	export default {
        components:{
            TableComponent,
			uniIcons
        },
		data() {
			return {
		
			}
		},
		onLoad() {	
		},
		mounted() {
	
		},
		methods: {

		}
	}


</script>
<style>
.content{
    background: #b7b7b7;
    width: 100%;
    height: 100vh;
    opacity: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
.up{
	display: flex;
    background: rgb(137, 186, 249);
    height: 300rpx;
    width: 95%;
    opacity: 1;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    align-items: center;
	flex-direction:column;
	
}


.down{
    background: rgb(255, 255, 255);
    height: 83%;
    width: 95%;
    opacity: 1;
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
    display: flex;
    flex-direction: column;
    align-items: center
}
.title{
    font-size: 24px;  
    width: 80%;
    text-align: left;
	margin-top: 3%;
    
}
.class{
    font-size: 12px;  
    width: 80%;
    margin-top: 1%;
    text-align: left;

}
.picture{
    width: 95%;
    height: 15%;
    margin-top: 1%;
    margin-bottom: 2%;
    display:flex;
    flex-direction: row;
    overflow-x: auto;
    overflow-y: hidden;
    white-space: nowrap; /* 防止内容换行 */
}

</style>