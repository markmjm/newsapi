from datetime import datetime

from django.utils.timesince import timesince
from rest_framework import serializers
from news.models import Article, Journalist





class ArticleSerializer(serializers.ModelSerializer):
    time_since_publication = serializers.SerializerMethodField()
    # author = JournalistSerializer(read_only=True)
    # author = serializers.StringRelatedField()

    class Meta:
        model = Article
        exclude = ('id',)  # all but id
        # fields = '__all__'  # all
        # fields =('title', 'description', 'body') # a subset

    def get_time_since_publication(self, object):
        publication_date = object.publication_date
        now = datetime.now()
        time_delta = timesince(publication_date, now)
        return time_delta

    def validate(self, data):
        """check that description and title are defined"""
        if data["title"] == data["description"]:
            raise serializers.ValidationError("Title and Description must not be same")
        return data

    def validate_title(self, value):
        """check that title > 60"""
        if len(value) < 60:
            raise serializers.ValidationError("Title must be > 60 characters")
        return value

class JournalistSerializer(serializers.ModelSerializer):
    articles =  serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='article-detail')
    #articles = ArticleSerializer(read_only=True, many=True)
    class Meta:
        model = Journalist
        fields = '__all__'  # all
# class ArticleSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     author = serializers.CharField()
#     title = serializers.CharField()
#     description = serializers.CharField()
#     body = serializers.CharField()
#     location = serializers.CharField()
#     publication_date = serializers.DateField()
#     active = serializers.BooleanField()
#     created_at = serializers.DateTimeField(read_only=True)
#     updated_at = serializers.DateTimeField(read_only=True)
#
#     def create(self, validated_data):
#         print(validated_data)
#         return Article.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.author = validated_data.get('author', instance.author)
#         instance.title = validated_data.get('title', instance.title)
#         instance.description = validated_data.get('description', instance.description)
#         instance.body = validated_data.get('body', instance.body)
#         instance.publication_date = validated_data.get('publication_date', instance.publication_date)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
#
