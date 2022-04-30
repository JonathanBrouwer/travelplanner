<script lang="ts">
    import {RoutePoint} from "./data";

    export let route: RoutePoint;
</script>

<div class="rp">
    <div class="colour-wrapper">
        <div class="colour" style="background-color: {route.colour}"></div>
    </div>
    <div class="description">{route.description}</div>
</div>

<style>
    .colour-wrapper {
        grid-area: colour;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .colour {
        height: 25px;
        width: 25px;
        border-radius: 50%;
        display: inline-block;
    }

    .description {
        grid-area: description;
        display: flex;
        flex-direction: row;
        align-items: center;
    }

    .rp {
        width: 100%;
        height: 100%;
        display: grid;
        grid-template-columns: 5em auto;
        grid-template-rows: auto;
        grid-template-areas:
            "colour description"
            "colour subtext";
        background-color: transparent;
    }
</style>
