from rest_framework import serializers
from .models import Collection
from Users.serializers import CustomUserSerializer

class CollectionSerializer(serializers.ModelSerializer):
    recorded_by = CustomUserSerializer(read_only=True)

    class Meta:
        model = Collection
        fields = ['collection_id', 'code', 'name', 'type', 'amount', 'unit_code', 'recorded_by']
        read_only_fields = ['collection_id', 'unit_code', 'recorded_by']

    def validate(self, data):
        code = data.get('code')
        name = data.get('name')
        amount = data.get('amount')

        # Validate code
        if code is None or len(code) < 1 or len(code) > 11:
            raise serializers.ValidationError("Mã khoản thu phải từ 1 đến 11 ký tự")
        if self.instance is None and Collection.objects.filter(code=code).exists():
            raise serializers.ValidationError("Mã khoản thu đã bị trùng!")

        # Validate name
        if len(name) < 1 or len(name) > 50:
            raise serializers.ValidationError("Hãy nhập tên khoản thu hợp lệ (1-50 ký tự)!")

        # Validate amount
        if amount is None or amount <= 0 or amount >= 10**11:
            raise serializers.ValidationError("Hãy nhập số tiền hợp lệ (số nguyên dương, nhỏ hơn 11 chữ số)!")

        return data

    def create(self, validated_data):
        validated_data['recorded_by'] = self.context['request'].user
        validated_data['unit_code'] = self.context['request'].user.unit_code
        return Collection.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data['recorded_by'] = self.context['request'].user
        validated_data['unit_code'] = self.context['request'].user.unit_code
        return super().update(instance, validated_data)