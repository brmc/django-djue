{% autoescape off %}{% if html %}<template>
<div>
  {{ html }}
</div>
</template>

{% endif %}<script>
{{ js }}</script>
{% endautoescape %}