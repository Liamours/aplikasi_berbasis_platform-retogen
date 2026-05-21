import 'package:retogen/features/articles/utils/article_data_utils.dart';

class ArticleDetail {
  final String id;
  final String title;
  final String preview;
  final String content;
  final List<String> tags;
  final String? imageBase64;
  final String currentUserEmail;
  final String username;
  final List<ArticleComment> comments;
  final List<ArticleRating> ratings;
  final List<PriceEntry> prices;

  const ArticleDetail({
    required this.id,
    required this.title,
    required this.preview,
    required this.content,
    required this.tags,
    required this.imageBase64,
    required this.currentUserEmail,
    required this.username,
    required this.comments,
    required this.ratings,
    required this.prices,
  });

  factory ArticleDetail.fromJson(
    String id,
    Map<String, dynamic> json, {
    List<PriceEntry> prices = const [],
  }) {
    final content = json['article_content']?.toString() ?? '';
    final preview = json['article_preview']?.toString().trim();

    return ArticleDetail(
      id: id,
      title: json['article_title']?.toString() ?? 'Artikel',
      preview: (preview != null && preview.isNotEmpty)
          ? preview
          : deriveArticlePreview(content),
      content: content,
      tags: asStringList(json['article_tags']),
      imageBase64: json['article_image']?.toString(),
      currentUserEmail: json['user_email']?.toString() ?? '',
      username: json['username']?.toString() ?? '',
      comments: asMapList(
        json['comments'],
      ).map(ArticleComment.fromJson).toList(),
      ratings: asMapList(json['ratings']).map(ArticleRating.fromJson).toList(),
      prices: prices,
    );
  }

  ArticleDetail copyWith({List<PriceEntry>? prices}) {
    return ArticleDetail(
      id: id,
      title: title,
      preview: preview,
      content: content,
      tags: tags,
      imageBase64: imageBase64,
      currentUserEmail: currentUserEmail,
      username: username,
      comments: comments,
      ratings: ratings,
      prices: prices ?? this.prices,
    );
  }

  int get totalComments => comments.length;

  double get averageRating {
    if (ratings.isEmpty) return 0;
    final total = ratings.fold<int>(0, (sum, rating) => sum + rating.value);
    return total / ratings.length;
  }

  String get averageRatingText => averageRating.toStringAsFixed(1);

  List<String> get paragraphs {
    return content
        .split(RegExp(r'\n\s*\n'))
        .map((paragraph) => paragraph.trim())
        .where((paragraph) => paragraph.isNotEmpty)
        .toList();
  }

  PriceEntry? get lowestPrice {
    if (prices.isEmpty) return null;
    final sorted = [...prices]..sort((a, b) => a.price.compareTo(b.price));
    return sorted.first;
  }

  List<PriceEntry> get topRatedPrices {
    final sorted = [...prices]
      ..sort((a, b) {
        final ratingDiff = (b.rating ?? 0).compareTo(a.rating ?? 0);
        if (ratingDiff != 0) return ratingDiff;
        return a.price.compareTo(b.price);
      });
    return sorted.take(3).toList();
  }

  ArticleRating? get ratingByCurrentUser {
    if (currentUserEmail.isEmpty) return null;
    final email = currentUserEmail.toLowerCase();
    for (final rating in ratings) {
      if ((rating.userEmail ?? '').toLowerCase() == email) return rating;
    }
    return null;
  }

  int get currentUserRating => ratingByCurrentUser?.value ?? 0;

  int? ratingForEmail(String? email) {
    if (email == null) return null;
    final normalized = email.toLowerCase();
    for (final rating in ratings) {
      if ((rating.userEmail ?? '').toLowerCase() == normalized) {
        return rating.value;
      }
    }
    return null;
  }

  List<ArticleComment> get commentTree {
    final map = <String, ArticleComment>{};
    final roots = <ArticleComment>[];

    for (final comment in comments) {
      map[comment.commentId] = comment.copyWith(children: []);
    }

    for (final comment in map.values) {
      final parentId = comment.parentCommentId;
      if (parentId != null && map.containsKey(parentId)) {
        map[parentId]!.children.add(comment);
      } else {
        roots.add(comment);
      }
    }

    return roots;
  }
}

class ArticleComment {
  final String commentId;
  final String? parentCommentId;
  final String owner;
  final String? userEmail;
  final String content;
  final List<ArticleComment> children;

  const ArticleComment({
    required this.commentId,
    required this.parentCommentId,
    required this.owner,
    required this.userEmail,
    required this.content,
    this.children = const [],
  });

  factory ArticleComment.fromJson(Map<String, dynamic> json) {
    final parent = json['parent_comment_id']?.toString();

    return ArticleComment(
      commentId: json['comment_id']?.toString() ?? '',
      parentCommentId: parent == null || parent.isEmpty || parent == 'null'
          ? null
          : parent,
      owner: json['owner']?.toString() ?? 'Unknown',
      userEmail: json['user_email']?.toString(),
      content: json['comment_content']?.toString() ?? '',
    );
  }

  ArticleComment copyWith({List<ArticleComment>? children}) {
    return ArticleComment(
      commentId: commentId,
      parentCommentId: parentCommentId,
      owner: owner,
      userEmail: userEmail,
      content: content,
      children: children ?? this.children,
    );
  }
}

class ArticleRating {
  final String ratingId;
  final String? userEmail;
  final int value;

  const ArticleRating({
    required this.ratingId,
    required this.userEmail,
    required this.value,
  });

  factory ArticleRating.fromJson(Map<String, dynamic> json) {
    return ArticleRating(
      ratingId: json['rating_id']?.toString() ?? '',
      userEmail: json['user_email']?.toString(),
      value: (json['rating_value'] as num?)?.round() ?? 0,
    );
  }
}

class PriceEntry {
  final String id;
  final String? store;
  final String product;
  final num price;
  final num? rating;

  const PriceEntry({
    required this.id,
    required this.store,
    required this.product,
    required this.price,
    required this.rating,
  });

  factory PriceEntry.fromJson(Map<String, dynamic> json, int index) {
    return PriceEntry(
      id: 'price-$index',
      store: json['store']?.toString(),
      product: json['product']?.toString() ?? 'Produk',
      price: json['price'] as num? ?? 0,
      rating: json['rating'] as num?,
    );
  }

  String get storeLabel {
    final label = store?.trim();
    return label == null || label.isEmpty ? 'Tokopedia' : label;
  }

  String get storeInitial =>
      storeLabel.isEmpty ? 'T' : storeLabel[0].toUpperCase();

  String get ratingText {
    final value = rating;
    if (value == null) return 'Belum ada';
    return value.toStringAsFixed(1);
  }
}
