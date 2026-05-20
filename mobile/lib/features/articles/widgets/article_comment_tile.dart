import 'package:flutter/material.dart';
import 'package:retogen/core/theme.dart';
import 'package:retogen/features/articles/models/article_detail.dart';
import 'package:retogen/features/articles/widgets/article_detail_shell.dart';

class ArticleCommentTile extends StatelessWidget {
  final ArticleComment comment;
  final ArticleDetail article;
  final bool isOwn;
  final String? activeReplyId;
  final String? activeEditId;
  final TextEditingController replyController;
  final TextEditingController editController;
  final bool isSaving;
  final bool isChild;
  final void Function(String commentId) onToggleReply;
  final void Function(String commentId) onSubmitReply;
  final void Function(ArticleComment comment) onStartEdit;
  final VoidCallback onCancelEdit;
  final Future<void> Function(ArticleComment comment) onSaveEdit;
  final Future<void> Function(ArticleComment comment) onDelete;
  final Future<void> Function(ArticleComment comment) onReport;
  final TextEditingController Function(String commentId) resolveReplyController;
  final bool Function(ArticleComment comment) isOwnComment;

  const ArticleCommentTile({
    super.key,
    required this.comment,
    required this.article,
    required this.isOwn,
    required this.activeReplyId,
    required this.activeEditId,
    required this.replyController,
    required this.editController,
    required this.isSaving,
    required this.onToggleReply,
    required this.onSubmitReply,
    required this.onStartEdit,
    required this.onCancelEdit,
    required this.onSaveEdit,
    required this.onDelete,
    required this.onReport,
    required this.resolveReplyController,
    required this.isOwnComment,
    this.isChild = false,
  });

  @override
  Widget build(BuildContext context) {
    final isReplying = activeReplyId == comment.commentId;
    final isEditing = activeEditId == comment.commentId;
    final canReply = !isChild && !isEditing;
    final userRating = article.ratingForEmail(comment.userEmail);

    return Container(
      padding: EdgeInsets.all(isChild ? 12 : 14),
      decoration: BoxDecoration(
        color: isChild
            ? AppTheme.primaryCyan.withValues(alpha: 0.04)
            : AppTheme.bgSurface.withValues(alpha: 0.76),
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: AppTheme.glassBorder),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _CommentAvatar(owner: comment.owner),
              const SizedBox(width: 10),
              Expanded(
                child: _CommentAuthor(
                  owner: comment.owner,
                  userRating: userRating,
                ),
              ),
              _CommentActionsMenu(
                isOwn: isOwn,
                onEdit: () => onStartEdit(comment),
                onDelete: () => onDelete(comment),
                onReport: () => onReport(comment),
              ),
            ],
          ),
          const SizedBox(height: 12),
          if (isEditing)
            _buildEditBox()
          else
            Text(
              comment.content,
              style: const TextStyle(
                color: AppTheme.textPrimary,
                fontSize: 14,
                height: 1.65,
              ),
            ),
          if (canReply) ...[
            const SizedBox(height: 8),
            Align(
              alignment: Alignment.centerRight,
              child: TextButton.icon(
                onPressed: () => onToggleReply(comment.commentId),
                icon: Icon(isReplying ? Icons.close : Icons.reply, size: 16),
                label: Text(isReplying ? 'Tutup' : 'Balas'),
                style: TextButton.styleFrom(
                  foregroundColor: AppTheme.primaryRed,
                  visualDensity: VisualDensity.compact,
                  tapTargetSize: MaterialTapTargetSize.shrinkWrap,
                  padding: const EdgeInsets.symmetric(horizontal: 8),
                ),
              ),
            ),
          ],
          if (isReplying && !isEditing) ...[
            const SizedBox(height: 12),
            _buildReplyBox(),
          ],
          if (comment.children.isNotEmpty) ...[
            const SizedBox(height: 12),
            Column(
              children: comment.children
                  .map(
                    (child) => Padding(
                      padding: const EdgeInsets.only(bottom: 10),
                      child: ArticleCommentTile(
                        comment: child,
                        article: article,
                        isOwn: isOwnComment(child),
                        activeReplyId: activeReplyId,
                        activeEditId: activeEditId,
                        replyController: resolveReplyController(
                          child.commentId,
                        ),
                        editController: editController,
                        isSaving: isSaving,
                        isChild: true,
                        onToggleReply: onToggleReply,
                        onSubmitReply: onSubmitReply,
                        onStartEdit: onStartEdit,
                        onCancelEdit: onCancelEdit,
                        onSaveEdit: onSaveEdit,
                        onDelete: onDelete,
                        onReport: onReport,
                        resolveReplyController: resolveReplyController,
                        isOwnComment: isOwnComment,
                      ),
                    ),
                  )
                  .toList(),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildReplyBox() {
    return _CommentInputBox(
      controller: replyController,
      hintText: 'Tulis balasan singkat...',
      minLines: 3,
      isSaving: isSaving,
      cancelLabel: 'Batal',
      submitLabel: 'Kirim',
      onCancel: () => onToggleReply(comment.commentId),
      onSubmit: () => onSubmitReply(comment.commentId),
    );
  }

  Widget _buildEditBox() {
    return _CommentInputBox(
      controller: editController,
      hintText: 'Edit komentar',
      minLines: 4,
      isSaving: isSaving,
      cancelLabel: 'Batal',
      submitLabel: 'Simpan',
      onCancel: onCancelEdit,
      onSubmit: () => onSaveEdit(comment),
    );
  }
}

class _CommentAvatar extends StatelessWidget {
  final String owner;

  const _CommentAvatar({required this.owner});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 38,
      height: 38,
      decoration: BoxDecoration(
        color: Colors.white.withValues(alpha: 0.18),
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: AppTheme.glassBorder),
      ),
      alignment: Alignment.center,
      child: Text(
        owner.isEmpty ? '?' : owner[0].toUpperCase(),
        style: const TextStyle(
          color: AppTheme.textPrimary,
          fontWeight: FontWeight.w800,
        ),
      ),
    );
  }
}

class _CommentAuthor extends StatelessWidget {
  final String owner;
  final int? userRating;

  const _CommentAuthor({required this.owner, required this.userRating});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          owner,
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
          softWrap: false,
          style: const TextStyle(
            color: AppTheme.primaryRed,
            fontSize: 14,
            fontWeight: FontWeight.w800,
          ),
        ),
        if (userRating != null) ...[
          const SizedBox(height: 3),
          Text(
            '$userRating/5',
            style: const TextStyle(
              color: AppTheme.primaryRed,
              fontSize: 12,
              fontWeight: FontWeight.w700,
            ),
          ),
        ],
      ],
    );
  }
}

class _CommentActionsMenu extends StatelessWidget {
  final bool isOwn;
  final VoidCallback onEdit;
  final VoidCallback onDelete;
  final VoidCallback onReport;

  const _CommentActionsMenu({
    required this.isOwn,
    required this.onEdit,
    required this.onDelete,
    required this.onReport,
  });

  @override
  Widget build(BuildContext context) {
    return PopupMenuButton<String>(
      tooltip: 'Menu aksi',
      icon: const Icon(Icons.more_horiz),
      onSelected: (value) {
        switch (value) {
          case 'edit':
            onEdit();
            break;
          case 'delete':
            onDelete();
            break;
          case 'report':
            onReport();
            break;
        }
      },
      itemBuilder: (context) {
        return [
          if (isOwn)
            const PopupMenuItem(value: 'edit', child: Text('Edit komentar')),
          if (isOwn)
            const PopupMenuItem(value: 'delete', child: Text('Hapus komentar')),
          if (!isOwn)
            const PopupMenuItem(
              value: 'report',
              child: Text('Laporkan komentar'),
            ),
        ];
      },
    );
  }
}

class _CommentInputBox extends StatelessWidget {
  final TextEditingController controller;
  final String hintText;
  final int minLines;
  final bool isSaving;
  final String cancelLabel;
  final String submitLabel;
  final VoidCallback onCancel;
  final VoidCallback onSubmit;

  const _CommentInputBox({
    required this.controller,
    required this.hintText,
    required this.minLines,
    required this.isSaving,
    required this.cancelLabel,
    required this.submitLabel,
    required this.onCancel,
    required this.onSubmit,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: AppTheme.primaryCyan.withValues(alpha: 0.06),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AppTheme.primaryCyan.withValues(alpha: 0.14)),
      ),
      child: Column(
        children: [
          ArticleMultilineField(
            controller: controller,
            hintText: hintText,
            minLines: minLines,
          ),
          const SizedBox(height: 10),
          Row(
            children: [
              Expanded(
                child: OutlinedButton(
                  onPressed: isSaving ? null : onCancel,
                  child: Text(cancelLabel),
                ),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: FilledButton(
                  onPressed: isSaving ? null : onSubmit,
                  style: FilledButton.styleFrom(
                    backgroundColor: AppTheme.primaryCyan,
                  ),
                  child: Text(submitLabel),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
