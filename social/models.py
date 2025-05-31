from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from food_analysis.models import PersonalFoodRecord
from restaurants.models import Restaurant

class Friendship(models.Model):
    """好友關係模型"""
    STATUS_CHOICES = [
        ('pending', '待確認'),
        ('accepted', '已接受'),
        ('blocked', '已封鎖'),
    ]
    
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('from_user', 'to_user')
        
    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username} ({self.status})"

class SocialPost(models.Model):
    """社交動態模型"""
    POST_TYPES = [
        ('food_record', '飲食記錄'),
        ('restaurant_review', '餐廳評價'),
        ('achievement', '成就分享'),
        ('text', '文字動態'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    post_type = models.CharField(max_length=20, choices=POST_TYPES)
    content = models.TextField()
    image = models.ImageField(upload_to='social_posts/', blank=True, null=True)
    
    # 關聯的記錄
    food_record = models.ForeignKey(PersonalFoodRecord, on_delete=models.CASCADE, blank=True, null=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, blank=True, null=True)
    
    # 隱私設定
    is_public = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.user.username} - {self.get_post_type_display()}"

class PostLike(models.Model):
    """動態點讚模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(SocialPost, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'post')
        
    def __str__(self):
        return f"{self.user.username} 讚了 {self.post.user.username} 的動態"

class PostComment(models.Model):
    """動態評論模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(SocialPost, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        
    def __str__(self):
        return f"{self.user.username} 評論了 {self.post.user.username} 的動態"

class FoodGroup(models.Model):
    """飲食群組模型"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='group_images/', blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    members = models.ManyToManyField(User, through='GroupMembership', related_name='joined_groups')
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class GroupMembership(models.Model):
    """群組成員關係模型"""
    ROLE_CHOICES = [
        ('admin', '管理員'),
        ('moderator', '版主'),
        ('member', '成員'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(FoodGroup, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'group')
        
    def __str__(self):
        return f"{self.user.username} - {self.group.name} ({self.get_role_display()})"

class GroupChallenge(models.Model):
    """群組挑戰模型"""
    CHALLENGE_TYPES = [
        ('calorie_limit', '熱量控制'),
        ('protein_goal', '蛋白質目標'),
        ('vegetarian_days', '素食天數'),
        ('water_intake', '飲水量'),
        ('exercise_calories', '運動消耗'),
    ]
    
    group = models.ForeignKey(FoodGroup, on_delete=models.CASCADE, related_name='challenges')
    title = models.CharField(max_length=100)
    description = models.TextField()
    challenge_type = models.CharField(max_length=20, choices=CHALLENGE_TYPES)
    target_value = models.FloatField()  # 目標值
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, through='ChallengeParticipation', related_name='challenges')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.group.name} - {self.title}"

class ChallengeParticipation(models.Model):
    """挑戰參與記錄模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(GroupChallenge, on_delete=models.CASCADE)
    current_progress = models.FloatField(default=0)
    is_completed = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        unique_together = ('user', 'challenge')
        
    def __str__(self):
        return f"{self.user.username} - {self.challenge.title}"

class UserProfile(models.Model):
    """用戶社交資料模型"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='social_profile')
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    
    # 隱私設定
    show_email = models.BooleanField(default=False)
    show_location = models.BooleanField(default=True)
    show_birth_date = models.BooleanField(default=False)
    
    # 統計數據
    total_posts = models.IntegerField(default=0)
    total_likes_received = models.IntegerField(default=0)
    total_friends = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} 的社交資料"

class Notification(models.Model):
    """通知模型"""
    NOTIFICATION_TYPES = [
        ('friend_request', '好友請求'),
        ('friend_accepted', '好友請求已接受'),
        ('post_like', '動態點讚'),
        ('post_comment', '動態評論'),
        ('group_invite', '群組邀請'),
        ('group_join', '加入群組'),
        ('group_leave', '離開群組'),
        ('challenge_invite', '挑戰邀請'),
        ('message', '新訊息'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications', null=True, blank=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=100)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # 關聯對象
    related_post = models.ForeignKey(SocialPost, on_delete=models.CASCADE, null=True, blank=True)
    related_group = models.ForeignKey(FoodGroup, on_delete=models.CASCADE, null=True, blank=True)
    related_challenge = models.ForeignKey(GroupChallenge, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.recipient.username} - {self.title}'

class ChatRoom(models.Model):
    """聊天室模型"""
    ROOM_TYPES = [
        ('private', '私人聊天'),
        ('group', '群組聊天'),
    ]
    
    name = models.CharField(max_length=100, blank=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES, default='private')
    participants = models.ManyToManyField(User, related_name='chat_rooms')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    # 群組聊天室可以關聯到飲食群組
    related_group = models.OneToOneField(FoodGroup, on_delete=models.CASCADE, null=True, blank=True, related_name='chat_room')
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        if self.name:
            return self.name
        elif self.room_type == 'private':
            participants = list(self.participants.all()[:2])
            if len(participants) == 2:
                return f'{participants[0].username} & {participants[1].username}'
        return f'聊天室 #{self.id}'
    
    def get_last_message(self):
        """獲取最後一條訊息"""
        return self.messages.first()
    
    def get_unread_count(self, user):
        """獲取用戶未讀訊息數量"""
        return self.messages.filter(is_read=False).exclude(sender=user).count()

class ChatMessage(models.Model):
    """聊天訊息模型"""
    MESSAGE_TYPES = [
        ('text', '文字訊息'),
        ('image', '圖片訊息'),
        ('file', '檔案訊息'),
        ('system', '系統訊息'),
    ]
    
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES, default='text')
    content = models.TextField()
    image = models.ImageField(upload_to='chat_images/', null=True, blank=True)
    file = models.FileField(upload_to='chat_files/', null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(null=True, blank=True)
    
    # 回覆功能
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.sender.username}: {self.content[:50]}...'
    
    def mark_as_read(self):
        """標記為已讀"""
        if not self.is_read:
            self.is_read = True
            self.save()

class ChatRoomMembership(models.Model):
    """聊天室成員關係"""
    ROLES = [
        ('member', '成員'),
        ('admin', '管理員'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    last_read_at = models.DateTimeField(auto_now_add=True)
    is_muted = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['user', 'room']
    
    def __str__(self):
        return f'{self.user.username} in {self.room}'
