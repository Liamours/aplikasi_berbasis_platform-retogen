import 'package:flutter/material.dart';
import 'package:retogen/core/api_client.dart';

class ArticlesPage extends StatefulWidget {
  const ArticlesPage({super.key});

  @override
  State<ArticlesPage> createState() => _ArticlesPageState();
}

class _ArticlesPageState extends State<ArticlesPage> {
  List<dynamic> _articles = [];
  bool _loading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _fetchArticles();
  }

  Future<void> _fetchArticles() async {
    try {
      final res = await ApiClient.instance.post('/get_main_page', data: {
        'search': '',
        'tag': '',
        'sort': 'newest',
      });
      setState(() {
        _articles = res.data['articles'] ?? [];
        _loading = false;
      });
    } catch (e) {
      setState(() { _error = 'Failed to load articles'; _loading = false; });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('RetoGen')),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : _error != null
              ? Center(child: Text(_error!))
              : RefreshIndicator(
                  onRefresh: _fetchArticles,
                  child: ListView.builder(
                    itemCount: _articles.length,
                    itemBuilder: (ctx, i) {
                      final a = _articles[i];
                      return Card(
                        margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                        child: ListTile(
                          title: Text(a['title'] ?? '', style: const TextStyle(fontWeight: FontWeight.bold)),
                          subtitle: Text('${a['owner_username'] ?? ''} • ${(a['tags'] as List?)?.join(', ') ?? ''}'),
                          trailing: Text('⭐ ${(a['average_rating'] ?? 0).toStringAsFixed(1)}'),
                        ),
                      );
                    },
                  ),
                ),
    );
  }
}
