{% autoescape off %}{% if html %}<template>
  {{ html }}
</template>

{% endif %}<script>
{{ js }}</script>
{% endautoescape %}