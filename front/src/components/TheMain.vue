<script setup>
import { nextTick, ref, computed } from 'vue'
import { NCard, NH2, NH1, NH3, NTag, NUpload, NButton } from 'naive-ui'
import { useImageStore } from '@/stores/useImageStore'
import placeholderImage from '@/assets/placeholder.json'
import BaseLoader from '@/components/BaseLoader.vue'

const imageStore = useImageStore()

const classes = ref({
    adj: 'Прилегающие дефекты',
    int: 'Дефекты целостности',
    geo: 'Дефекты геометрии',
    pro: 'Дефекты постобработки',
    non: 'Дефекты невыполнения'
})

const fillRectangles = async () => {
    if (!Array.isArray(imageStore.result.objects)) return
    await nextTick()
    const img = document.querySelector('#img-result')
    const imgWrapper = document.querySelector('.img-result-wrapper')
    const bounding = img.getBoundingClientRect()
    const width = bounding.width
    const height = bounding.height
    const actualWidth = 640
    const actualHeight = 640
    const coeffX = width / actualWidth
    const coeffY = height / actualHeight

    imageStore.result.objects.forEach((obj) => {
        const newX = obj.x * coeffX
        const newY = obj.y * coeffY
        const newWidth = obj.width * coeffX
        const newHeight = obj.height * coeffY

        const left = `${newX - newWidth / 2}px`
        const top = `${newY - newHeight / 2}px`

        const rect = document.createElement('div')
        rect.style.left = left
        rect.style.top = top
        rect.style.width = newWidth + 'px'
        rect.style.height = newHeight + 'px'
        rect.classList.add('image-rect')

        const text = document.createElement('div')
        text.classList.add('image-text')
        text.style.left = left
        text.style.top = `${newY + newHeight / 2}px`
        text.innerText = obj.class

        imgWrapper.insertAdjacentElement('beforeend', rect)
        imgWrapper.insertAdjacentElement('beforeend', text)
    })
}

const handleUpload = async ({ file }) => {
    try {
        imageStore.startLoading()
        imageStore.setImage(file)

        const formData = new FormData()
        formData.append('file', imageStore.image.file)
        const response = await fetch('http://178.154.206.195/photoRec', {
            method: 'POST',
            body: formData
        })

        const data = await response.json()

        imageStore.setResult(data)
        fillRectangles()
    } catch {
        imageStore.setResult(placeholderImage)
    } finally {
        imageStore.stopLoading()
    }
}
</script>

<template>
    <div class="main-content">
        <NCard class="main-content-image">
            <template #header>Результат на изображении</template>
            <div class="img-result-wrapper">
                <img
                    v-if="imageStore.imageURL"
                    id="img-result"
                    :src="imageStore.imageURL"
                    class="main-image"
                    @load="fillRectangles"
                />
            </div>
        </NCard>

        <NCard class="main-content-result">
            <template v-if="imageStore.hasResult" #header>Результаты</template>
            <template v-else #header> Загрузите фотографию для распознавания </template>
            <div v-if="!imageStore.hasResult">
                <div class="upload-content">
                    <NUpload class="upload-component" :custom-request="handleUpload">
                        <NButton type="primary" size="large">Выбрать</NButton>
                    </NUpload>
                    <BaseLoader v-if="imageStore.isLoading" />
                </div>
            </div>
            <div v-else style="margin-bottom: 20px;" v-for="(obj, index) in imageStore.result.objects" :key="index">
                <NH1 v-if="imageStore.result.objects.length > 1">Деффект шва #{{ index + 1 }}</NH1>
                <div class="main-info">
                    <NTag type="info" size="large" round :bordered="false">
                        Координаты: ({{ obj.x }}, {{ obj.y }})
                    </NTag>
                    <NTag type="info" size="large" round :bordered="false">
                        Ширина: {{ obj.width }}
                    </NTag>
                    <NTag type="info" size="large" round :bordered="false">
                        Высота: {{ obj.height }}
                    </NTag>
                    <NTag type="info" size="large" round :bordered="false">
                        Класс: {{ obj.class }} ({{ classes[obj.class] }})
                    </NTag>
                </div>
            </div>
        </NCard>
    </div>
    <NButton
        v-if="imageStore.hasResult"
        @click="imageStore.reset"
        type="primary"
        ghost
        block
        class="reset-btn"
    >
        Сбросить фотографию
    </NButton>
    <!-- <NCard class="json-content" v-if="imageStore.hasResult">
        <template #header>Результат (json)</template>
        <NCode :code="imageStore.resultJSON" language="json" />
    </NCard> -->
</template>

<style>
.main-content {
    display: flex;
    flex-direction: column;
    justify-content: center;

    align-items: center;

    flex-wrap: nowrap;
    padding: 15px 0;
    gap: 20px;
    overflow: auto;
}

.main-content-image {
    width: auto;
}

.main-content-result {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}

.main-info {
    display: flex;

    flex-wrap: wrap;

    gap: 10px;
}

.main-digit {
    margin-top: 20px;
}

.main-image {
    width: 640px;
    height: 640px;
}

@media (max-width: 980px) {
    .main-content {
        flex-direction: column;
    }

    .main-content-image {
        width: 100%;
    }

    .main-image {
        max-width: 100%;
        height: auto;
    }
}

.img-result-wrapper {
    position: relative;
}

.image-rect {
    position: absolute;

    box-sizing: border-box !important;

    display: v-bind('numberDisplay');

    border: 2px solid red;
}

.image-text {
    position: absolute;

    box-sizing: border-box !important;

    display: v-bind('numberDisplay');

    color: red;
    font-size: 16px;
    background-color: #00000099;
    line-height: 1;
}

.image-rect-digit {
    position: absolute;

    box-sizing: border-box !important;

    display: v-bind('digitDisplay');

    border: 2px solid blue;
}

.img-control {
    display: flex;

    flex-direction: column;

    gap: 10px;

    margin-top: 20px;
}

.reset-btn {
    height: 60px;
    margin-bottom: 20px;
}
</style>
